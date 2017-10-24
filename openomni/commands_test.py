import unittest

import commands

class CommandsTestCase(unittest.TestCase):

    def test_parse_unknown_command(self):
        # Parse a 0x99 command with length 0x01
        cmd, _ = commands.parse_command("990100".decode("hex"))
        self.assertTrue(isinstance(cmd, commands.UnknownCommand))

    def test_parse_cancel(self):
        # Parse cancel temp basal from PDM
        cmd, _ = commands.parse_command("1f05156b93e8620028".decode("hex"))
        self.assertTrue(isinstance(cmd, commands.CancelCommand))

    def test_parse_1d_response(self):
        resp, _ = commands.parse_command("1d18003e980000421fff".decode("hex"))
        self.assertTrue(isinstance(resp, commands.PodStatusResponse))
        self.assertEqual(resp.minutes_active, 135)
        self.assertEqual(resp.reservoir_level, 50.0)

    def test_parse_01_response(self):
        """Test 0x01 command parsing.
        Values from https://github.com/openaps/openomni/wiki/Response-01
        """
        fmt1, _ = commands.parse_command("011b13881008340a5002070002070002030000a3770003ab371f00ee87".decode("hex"))
        fmt2a, _ = commands.parse_command("011502070002070002020000a3770003ab379f1f00ee87".decode("hex"))
        fmt2b, _ = commands.parse_command("011502070002070002020000a64000097c279c1f08ced2".decode("hex"))
        for m in (fmt1, fmt2a, fmt2b):
            self.assertTrue(isinstance(m, commands.Message01Response))
        self.assertEqual(fmt1.hardcode_bytes, "13881008340a5002070002070002")
        self.assertEqual(fmt1.state_byte, "03")
        self.assertEqual(fmt1.lot, "0000a377")
        self.assertEqual(fmt1.tid, "0003ab37")
        self.assertEqual(fmt1.pod_address, "1f00ee87")

        self.assertEqual(fmt2a.hardcode_bytes, "02070002070002")
        self.assertEqual(fmt2a.state_byte, "02")
        self.assertEqual(fmt2a.lot, "0000a377")
        self.assertEqual(fmt2a.tid, "0003ab37")
        self.assertEqual(fmt2a.pod_address, "1f00ee87")

        self.assertEqual(fmt2b.hardcode_bytes, "02070002070002")
        self.assertEqual(fmt2b.state_byte, "02")
        self.assertEqual(fmt2b.lot, "0000a640")
        self.assertEqual(fmt2b.tid, "00097c27")
        self.assertEqual(fmt2b.pod_address, "1f08ced2")


if __name__ == "__main__":
    unittest.main()
