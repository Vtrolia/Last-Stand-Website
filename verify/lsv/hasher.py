from django.contrib.auth.hashers import BasePasswordHasher, mask_hash
from django.utils.translation import gettext_noop as _
import hashlib as h

class sha256Hasher(BasePasswordHasher):
    """
    A somewhat secure algorithm that you probably shouldn't use, but it's all
    that I could get my C program to work with.
    """
    algorithm = "sha256"
    
    def salt(self):
        return ""
    
    def encode(self, password, salt):
        assert salt == ""
        result = h.sha256(password.encode()).hexdigest()
        return "sha256$$%s" % result
    
    def verify(self, password, encoded):
        attempted = self.encode(password, "")
        return attempted == encoded
    
    def safe_summary(self, encoded):
        algorithm, salt, data = encoded.split("$", 2)
        assert algorithm == self.algorithm
        return {
            _('algorithm'): algorithm,
            _('salt'): salt,
            _('hash'): mask_hash(data, show=3),
        }
    
    def harden_runtime(self, password, encoded):
        pass
    
