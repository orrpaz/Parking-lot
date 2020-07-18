import logging

logger = logging.getLogger()

# ...

def foo(num):
    if num == 1:
        logger.warning('One is not acepted')
        return False
    # Do somenthing ...
    return True

# ...

def test_foo(self):
    with self.assertLogs('backend', level='INFO') as cm:
        result = self.foo(1)
    self.assertFalse(result)
    self.assertIn('WARNING:backend:One is not acepted', cm.output)

print("ffff")
print("gdfgdfg")