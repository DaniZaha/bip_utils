# Copyright (c) 2021 Emanuele Bellocchia
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""Module with utility functions for address decoding."""

# Imports
from typing import Callable, overload, Tuple, Type, Union
from bip_utils.ecc import IPublicKey
from bip_utils.utils.misc import BytesUtils


class AddrDecUtils:
    """Class container for address decoding utility functions."""

    @staticmethod
    @overload
    def ValidateAndRemovePrefix(addr: bytes,
                                prefix: bytes) -> bytes:
        ...

    @staticmethod
    @overload
    def ValidateAndRemovePrefix(addr: str,
                                prefix: str) -> str:
        ...

    @staticmethod
    def ValidateAndRemovePrefix(addr: Union[bytes, str],
                                prefix: Union[bytes, str]) -> Union[bytes, str]:
        """
        Validate and remove prefix from an address.

        Args:
            addr (bytes or str)  : Address string or bytes
            prefix (bytes or str): Address prefix

        Returns:
            bytes or str: Address string or bytes with prefix removed

        Raises:
            ValueError: If the prefix is not valid
        """
        prefix_got = addr[:len(prefix)]
        if prefix != prefix_got:
            raise ValueError(f"Invalid prefix (expected {prefix!r}, got {prefix_got!r})")
        return addr[len(prefix):]

    @staticmethod
    def ValidateLength(addr: Union[bytes, str],
                       expected_len: int) -> None:
        """
        Validate address length.

        Args:
            addr (str)        : Address string or bytes
            expected_len (int): Expected address length

        Raises:
            ValueError: If the length is not valid
        """
        if len(addr) != expected_len:
            raise ValueError(f"Invalid length {len(addr)}")

    @staticmethod
    def ValidatePubKey(pub_key_bytes: bytes,
                       pub_key_cls: Type[IPublicKey]) -> None:
        """
        Validate address length.

        Args:
            pub_key_bytes (bytes)   : Public key bytes
            pub_key_cls (IPublicKey): Public key class type

        Raises:
            ValueError: If the public key is not valid
        """
        if not pub_key_cls.IsValidBytes(pub_key_bytes):
            raise ValueError(f"Invalid {pub_key_cls.CurveType()} "
                             f"public key {BytesUtils.ToHexString(pub_key_bytes)}")

    @staticmethod
    def ValidateChecksum(payload_bytes: bytes,
                         checksum_bytes_exp: bytes,
                         checksum_fct: Callable[[bytes], bytes]) -> None:
        """
        Validate address checksum.

        Args:
            payload_bytes (bytes)     : Payload bytes
            checksum_bytes_exp (bytes): Expected checksum bytes
            checksum_fct (function)   : Function for computing checksum

        Raises:
            ValueError: If the computed checksum is not equal tot he specified one
        """
        checksum_bytes_got = checksum_fct(payload_bytes)
        if checksum_bytes_exp != checksum_bytes_got:
            raise ValueError(f"Invalid checksum (expected {BytesUtils.ToHexString(checksum_bytes_exp)}, "
                             f"got {BytesUtils.ToHexString(checksum_bytes_got)})")

    @staticmethod
    def SplitPartsByChecksum(addr_bytes: bytes,
                             checksum_len: int) -> Tuple[bytes, bytes]:
        """
        Split address in two parts, considering the checksum at the end of it.

        Args:
            addr_bytes (bytes): Address bytes
            checksum_len (int): Checksum length

        Returns:
            tuple: Payload bytes (index 0) and checksum bytes (index 1)
        """
        checksum_bytes = addr_bytes[-1 * checksum_len:]
        payload_bytes = addr_bytes[:-1 * checksum_len]
        return payload_bytes, checksum_bytes
