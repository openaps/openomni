"""Implement command handlers."""
from enum import Enum
import datetime


class _BaseCommand(object):
    """Base command implementation."""

    # The command ID this class handles
    COMMAND_ID = None

    def __init__(self, data, command_id=None, command_length=None):
        self.command_id = command_id
        self.command_length = command_length
        self.data = data
        try:
            self.populate()
        except NotImplementedError:
            pass

    def populate(self):
        """Assembles this packet from self.data."""
        raise NotImplementedError

    def debug_detail(self):
        """Returns the body of the printed packet, PacketType(debug_detail)."""
        return self.data.encode("hex")

    def __str__(self):
        return "%s-%02x(%s)" % (
                self.__class__.__name__, self.command_id, self.debug_detail())

    def __repr__(self):
        return str(self)


class UnknownCommand(_BaseCommand):
    """Generic handler for unsupported commands."""


class InsulinScheduleCommand(_BaseCommand):
    """Represents the PDM command for scheduling insulin delivery."""

    COMMAND_ID = 0x1a

    class ScheduleTableType(Enum):
        """Represent the type of insulin delivery being configured."""
        BASAL = 0
        TEMP_RATE = 1
        BOLUS = 2

    def populate(self):
        self.nonce = self.data[0:4].encode("hex")
        self.table_num = ord(self.data[4])
        self.checksum = (ord(self.data[5]) << 8) + ord(self.data[6])
        self.duration = ord(self.data[7]) * 30
        self.field_a = self.data[8:10].encode("hex")
        self.rate = ((ord(self.data[10]) << 8) + ord(self.data[11])) * 0.1
        self.rate_schedule = self.data[12:14].encode("hex")

    def debug_detail(self):
        return ("nonce=%s, table=%s, checksum=%04x, duration=%dm, field_a=%s, rate=%fU/hr, rate_schedule=%s"
                % (self.nonce, self.ScheduleTableType(self.table_num).name, self.checksum, self.duration,
                    self.field_a, self.rate, self.rate_schedule))


class PodStatusResponse(_BaseCommand):
    """Handle pod status responses from the Pod to the PDM."""

    COMMAND_ID = 0x1d

    def populate(self):
        self.minutes_active = ((ord(self.data[5]) & 0x0f) << 6) + (ord(self.data[6]) >> 2)
        self.reservoir_level = round((float((((ord(self.data[6]) & 0x03) << 6) + (ord(self.data[7]) >> 2)))*50)/255, 0)

    def debug_detail(self):
        return "active_time=%s,reservoir_level=%sU" % (datetime.timedelta(minutes=self.minutes_active),self.reservoir_level)


class CancelCommand(_BaseCommand):
    """Handle cancel command variants."""

    COMMAND_ID = 0x1f


class Message01Response(_BaseCommand):

    COMMAND_ID = 0x01

    def populate(self):
        print len(self.data)
        print self.data.encode("hex")
        if self.command_length == 0x1b:
            self.hardcode_bytes = self.data[:14].encode("hex")
            self.state_byte = self.data[14].encode("hex")
            self.lot = self.data[15:19].encode("hex")
            self.tid = self.data[19:23].encode("hex")
            self.pod_address = self.data[23:27].encode("hex")
        elif self.command_length == 0x15:
            self.hardcode_bytes = self.data[:7].encode("hex")
            self.state_byte = self.data[7].encode("hex")
            self.lot = self.data[8:12].encode("hex")
            self.tid = self.data[12:16].encode("hex")
            self.rssi = self.data[16].encode("hex")
            self.pod_address = self.data[17:22].encode("hex")

    def debug_detail(self):
        if self.command_length == 0x1b:
            return ("length=0x1b,hardcode_bytes=%s,state_byte=%s,lot=%s,tid=%s,pod_address=%s"
                    % (self.hardcode_bytes, self.state_byte, self.lot, self.tid, self.pod_address))
        if self.command_length == 0x15:
            return ("length=0x15,hardcode_bytes=%s,state_byte=%s,lot=%s,tid=%s,rssi=%s,pod_address=%s"
                    % (self.hardcode_bytes, self.state_byte, self.lot, self.tid, self.rssi, self.pod_address))


# Build a dictionary of command IDs (eg 0x1a for InsulinScheduleCommand) to the
# class that implements their parsing
COMMAND_TYPES = {}
for cls in globals().values():
    if type(cls) == type and issubclass(cls, _BaseCommand) and cls.COMMAND_ID is not None:
	if cls.COMMAND_ID in COMMAND_TYPES:
	    raise Exception("%s is handled by more than one class! %s and %s"
			    % (cls.COMMAND_ID, cls, COMMAND_TYPES[command_id]))
	COMMAND_TYPES[cls.COMMAND_ID] = cls


def parse_command(body):
    """Parse a command out of a message body.

    Args:
       body: message body

    Returns:
       (command instance, remainder of the message body)
    """
    cmd_type = ord(body[0])
    cmd_len = ord(body[1])
    cmd_class = COMMAND_TYPES.get(cmd_type, UnknownCommand)
    instance = cmd_class(body[2:2+cmd_len], cmd_type, cmd_len)
    return (instance, body[2+cmd_len:])
