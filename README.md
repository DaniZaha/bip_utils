# BIP utility library
[![PyPI version](https://badge.fury.io/py/bip-utils.svg)](https://badge.fury.io/py/bip-utils)
[![Build Status](https://travis-ci.com/ebellocchia/bip_utils.svg?branch=master)](https://travis-ci.com/ebellocchia/bip_utils)
[![codecov](https://codecov.io/gh/ebellocchia/bip_utils/branch/master/graph/badge.svg)](https://codecov.io/gh/ebellocchia/bip_utils)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://raw.githubusercontent.com/ebellocchia/bip_utils/master/LICENSE)

## Introduction

This package contains an implementation of some BIP (Bitcoin Improvement Proposal) specifications, allowing to:
- Generate a mnemonic string from a random entropy
- Generate a secure seed from the mnemonic string
- Use the seed to generate the master key of the wallet and derive the children keys, including address encoding

The implemented BIP specifications are the following:
- [BIP-0039](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki) for mnemonic and seed generation
- [BIP-0032](https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki) for master key generation (from the secure seed) and children keys derivation
- [BIP-0044](https://github.com/bitcoin/bips/blob/master/bip-0044.mediawiki), [BIP-0049](https://github.com/bitcoin/bips/blob/master/bip-0049.mediawiki) and [BIP-0084](https://github.com/bitcoin/bips/blob/master/bip-0084.mediawiki) for the hierarchy of deterministic wallets, based on BIP-0032 specification

In addition to this, the package allows to:
- Parse BIP-0032 derivation paths
- Generate P2PKH addresses (included in BIP-0044)
- Generate P2SH addresses (included in BIP-0049)
- Generate P2WPKH addresses (included in BIP-0084)
- Generate Ethereum addresses
- Generate Ripple addresses
- Encode/Decode WIF
- Encode/Decode base58
- Encode/Decode bech32

The currently supported coins are:
- Bitcoin (and related test net)
- Litecoin (and related test net)
- Dogecoin (and related test net)
- Dash (and related test net)
- Ethereum
- Ripple

## Install the package

The package requires Python 3, it is not compatible with Python 2.
To install it:
- Using *setuptools*:

        python setup.py install

- Using *pip*:

        pip install bip_utils

To run the tests:

- Without code coverage

        python setup.py test

- With code coverage and report:

        pip install coverage
        coverage run -m unittest discover
        coverage report

## BIP-0039 library

### Mnemonic generation

A mnemonic string can be generated by specifying the words number (in this case a random entropy will be used) or directly the entropy bytes.\
Supported words number: *12, 15, 18, 21, 24*\
Supported entropy bits: *128, 160, 192, 224, 256*

**NOTE:** only the English words list is supported.

**Code example**

    import binascii
    from bip_utils import Bip39MnemonicGenerator

    # Generate a random mnemonic string of 15 words
    mnemonic = Bip39MnemonicGenerator.FromWordsNumber(15)

    # Generate the mnemonic string from entropy bytes:
    entropy_bytes_hex = b"00000000000000000000000000000000"
    mnemonic = Bip39MnemonicGenerator.FromEntropy(binascii.unhexlify(entropy_bytes_hex))

### Mnemonic validation

A mnemonic string can be validated by verifying its checksum.
It is also possible to get back the entropy bytes from a mnemonic.

**Code example**

     from bip_utils import Bip39MnemonicValidator

     # Get back the original entropy from a mnemonic string
     entropy_bytes = Bip39MnemonicValidator(mnemonic).GetEntropy()
     # Validate a mnemonic string by verifying its checksum
     is_valid = Bip39MnemonicValidator(mnemonic).Validate()

### Seed generation

A secure 64-byte seed is generated from a mnemonic and can be protected by a passphrase.\
This seed can be used to contruct a Bip class.

**Code example**

    from bip_utils import Bip39SeedGenerator

    # If not specified, the passphrase will be empty
    passphrase = "my_passphrase"
    seed_bytes = Bip39SeedGenerator(mnemonic).Generate(passphrase)

## BIP-0032 library

The BIP-0032 library is wrapped inside the BIP-0044, BIP-0049 and BIP-0084 libraries, so there is no need to use it alone unless you need to derive some non-standard paths.

### Construction from a seed

The class can be constructed from a seed. The seed can be specified manually or generated by *Bip39SeedGenerator*.\
The constructed class is the master path, so printing the private key will result in printing the master key.

**Code example**

    import binascii
    from bip_utils import Bip32

    # Seed bytes
    seed_bytes = binascii.unhexlify(b"5eb00bbddcf069084889a8ab9155568165f5c453ccb85e70811aaed6f6da5fc19a5ac40b389cd370d086206dec8aa6c43daea6690f20ad3d8d48b2d2ce9e38e4")
    # Construct from seed. In case it's a test net, pass True as second parameter. Derivation path returned: m
    bip32_ctx = Bip32.FromSeed(seed_bytes)
    # Print master key in extended format
    print(bip32_ctx.PrivateKey().ToExtended())

In addition to a seed, it's also possible to specify a derivation path.

**Code example**

    # Derivation path returned: m/0'/1'/2
    bip32_ctx = Bip32.FromSeedAndPath(seed_bytes, "m/0'/1'/2")
    # Print private key for derivation path m/0'/1'/2 in extended format
    print(bip32_ctx.PrivateKey().ToExtended())

### Construction from an extended key

Alternatively, the class can be constructed directly from an extended key.\
The object returned will be at the same depth of the specified key.

**Code example**

    from bip_utils import Bip32

    # Private extended key from derivation path m/0'/1 (depth 2)
    key_str = "xprv9wTYmMFdV23N2TdNG573QoEsfRrWKQgWeibmLntzniatZvR9BmLnvSxqu53Kw1UmYPxLgboyZQaXwTCg8MSY3H2EU4pWcQDnRnrVA1xe8fs"
    # Construct from key (return object has depth 2)
    bip32_ctx = Bip32.FromExtendedKey(key_str)
    # Print keys
    print(bip32_ctx.PrivateKey().ToExtended())
    print(bip32_ctx.PublicKey().ToExtended())

    # Public extended key from derivation path m/0'/1 (depth 2)
    key_str = "xpub6ASuArnXKPbfEwhqN6e3mwBcDTgzisQN1wXN9BJcM47sSikHjJf3UFHKkNAWbWMiGj7Wf5uMash7SyYq527Hqck2AxYysAA7xmALppuCkwQ"
    # Construct from key (return object has depth 2)
    bip32_ctx = Bip32.FromExtendedKey(key_str)
    # Print key
    print(bip32_ctx.PublicKey().ToExtended())
    # Getting private key from a public-only object triggers a Bip32KeyError exception

### Keys derivation

Each time a key is derived, a new instance of the Bip32 class is returned. This allows to chain the methods call or save a specific key pair for future derivation.\
The *Bip32Utils.HardenIndex* method can be used to make an index hardened.

**Code example**

    import binascii
    from bip_utils import Bip32, Bip32Utils

    # Seed bytes
    seed_bytes = binascii.unhexlify(b"5eb00bbddcf069084889a8ab9155568165f5c453ccb85e70811aaed6f6da5fc19a5ac40b389cd370d086206dec8aa6c43daea6690f20ad3d8d48b2d2ce9e38e4")
    # Path: m
    bip32_ctx = Bip32.FromSeed(seed_bytes)
    # Derivation path: m/0'/1'/2/3
    bip32_ctx = bip32_ctx.ChildKey(Bip32Utils.HardenIndex(0)) \
                         .ChildKey(Bip32Utils.HardenIndex(1)) \
                         .ChildKey(2)                         \
                         .ChildKey(3)
    # Print keys in extended format
    print(bip32_ctx.PrivateKey().ToExtended())
    print(bip32_ctx.PublicKey().ToExtended())
    # Print keys in hex format
    print(bip32_ctx.PrivateKey().Raw().ToHex())
    print(bip32_ctx.PublicKey().RawCompressed().ToHex())
    print(bip32_ctx.PublicKey().RawUncompressed().ToHex())
    # Print private key in WIF format
    print(bip32_ctx.PrivateKey().ToWif())
    # Print public key converted to address
    print(bip32_ctx.PublicKey().ToAddress())

    # Alternative: use DerivePath method
    bip32_ctx = Bip32.FromSeed(seed_bytes)
    bip32_ctx = bip32_ctx.DerivePath("0'/1'/2/3")

    # DerivePath derives from the current depth, so it can be split
    bip32_ctx = Bip32.FromSeed(seed_bytes)
    bip32_ctx = bip32_ctx.DerivePath("0'/1'")   # Derivation path: m/0'/1'
    bip32_ctx = bip32_ctx.DerivePath("2/3")     # Derivation path: m/0'/1'/2/3

### Parse path

The Bip32 module allows also to parse derivation paths by returning the list of indexes in the path.\
In case of error, an empty list is returned.

**Code example**

    from bip_utils import Bip32PathParser

    # Print: ["m", 2147483648, 2147483649, 2]
    print(Bip32PathParser.Parse("m/0'/1'/2"))
    # Same but skipping the master. Print: [2147483648, 2147483649, 2]
    print(Bip32PathParser.Parse("0'/1'/2", True))
    # 'p' can be used as an alternative character instead of '
    print(Bip32PathParser.Parse("m/0p/1p/2"))
    # Error path: empty list returned. Print: []
    print(Bip32PathParser.Parse("m/0'/abc/2"))

## Bip-0044, BIP-0049, BIP-0084 libraries

These libraries derives all from the same base class, so they are used exactly in the same way.\
Therefore, the following code examples can be used with the Bip44, Bip49 or Bip84 class.

### Construction from a seed

A Bip class can be constructed from a seed, like Bip32. The seed can be specified manually or generated by *Bip39SeedGenerator*.

**Code example**

    import binascii
    from bip_utils import Bip44, Bip44Coins

    # Seed bytes
    seed_bytes = binascii.unhexlify(b"5eb00bbddcf069084889a8ab9155568165f5c453ccb85e70811aaed6f6da5fc19a5ac40b389cd370d086206dec8aa6c43daea6690f20ad3d8d48b2d2ce9e38e4")
    # Derivation path returned: m
    # In case it's a test net, pass True as second parameter
    bip44_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.BITCOIN)

### Construction from an extended key

Alternatively, a Bip class can be constructed directly from an extended key.\
The Bip object returned will be at the same depth of the specified key.

**Code example**

    from bip_utils import Bip44, Bip44Coins

    # Private extended key
    key_str = "xprv9s21ZrQH143K3QTDL4LXw2F7HEK3wJUD2nW2nRk4stbPy6cq3jPPqjiChkVvvNKmPGJxWUtg6LnF5kejMRNNU3TGtRBeJgk33yuGBxrMPHi"
    # Construct from extended key
    bip44_ctx = Bip44.FromExtendedKey(key_str, Bip44Coins.BITCOIN)

### Keys derivation

Like Bip32, each time a key is derived a new instance of the Bip class is returned.\
The keys must be derived with the levels specified by BIP-0044:

    m / purpose' / coin_type' / account' / change / address_index

using the correspondent methods. If keys are derived in the wrong level, a *RuntimeError* will be raised.\
The private and public extended keys can be printed at any level.

Currently supported coins enumerative:
- Bitcoin (and related test net) : *Bip44Coins.BITCOIN, Bip44Coins.BITCOIN_TESTNET*
- Litecoin (and related test net) : *Bip44Coins.LITECOIN, Bip44Coins.LITECOIN_TESTNET*
- Dogecoin (and related test net) : *Bip44Coins.DOGECOIN, Bip44Coins.DOGECOIN_TESTNET*
- Dash (and related test net) : *Bip44Coins.DASH, Bip44Coins.DASH_TESTNET*
- Ethereum : *Bip44Coins.ETHEREUM*
- Ripple : *Bip44Coins.RIPPLE*

The library can be easily extended with other coins anyway.

**Code example**

    import binascii
    from bip_utils import Bip44, Bip44Coins, Bip44Changes

    # Seed bytes
    seed_bytes = binascii.unhexlify(b"5eb00bbddcf069084889a8ab9155568165f5c453ccb85e70811aaed6f6da5fc19a5ac40b389cd370d086206dec8aa6c43daea6690f20ad3d8d48b2d2ce9e38e4")
    # Create from seed
    bip44_mst = Bip44.FromSeed(seed_bytes, Bip44Coins.BITCOIN)

    # Print master key in extended format
    print(bip44_mst.PrivateKey().ToExtended())
    # Print master key in hex format
    print(bip44_mst.PrivateKey().Raw().ToHex())

    # Print public key in extended format (default: Bip44PubKeyTypes.EXT_KEY)
    print(bip44_mst.PublicKey())
    # Print public key in raw uncompressed format
    print(bip44_mst.PublicKey().RawUncompressed().ToHex())
    # Print public key in raw compressed format
    print(bip44_mst.PublicKey().RawCompressed().ToHex())

    # Print the master key in WIF
    print(bip44_mst.IsMasterLevel())
    print(bip44_mst.PrivateKey().ToWif())

    # Derive account 0 for Bitcoin: m/44'/0'/0'
    bip44_acc = bip44_mst.Purpose() \
                         .Coin()    \
                         .Account(0)
    # Print keys in extended format
    print(bip44_acc.IsAccountLevel())
    print(bip44_acc.PrivateKey().ToExtended())
    print(bip44_acc.PublicKey().ToExtended())

    # Derive the external chain: m/44'/0'/0'/0
    bip44_change = bip44_acc.Change(Bip44Changes.CHAIN_EXT)
    # Print again keys in extended format
    print(bip44_change.IsChangeLevel())
    print(bip44_change.PrivateKey().ToExtended())
    print(bip44_change.PublicKey().ToExtended())

    # Derive the first 20 addresses of the external chain: m/44'/0'/0'/0/i
    for i in range(20):
        bip44_addr = bip44_change.AddressIndex(i)
        # Print extended keys and address
        print(bip44_addr.PrivateKey().ToExtended())
        print(bip44_addr.PublicKey().ToExtended())
        print(bip44_addr.PublicKey().ToAddress())

In the example above, Bip44 can be substituted with Bip49 or Bip84 without changing the code.

## Ethereum/Ripple addresses

These libraries are used internally by the other libraries, but they are available also for external use.

**Code example**

    from bip_utils import EthAddr, XrpAddr

    # Ethereum needs the uncompressed public key
    addr = EthAddr.ToAddress(pub_key_bytes)
    # Ripple needs the compressed public key
    addr = XrpAddr.ToAddress(pub_key_bytes)

## P2PKH/P2SH/P2WPKH addresses

These libraries are used internally by the other libraries, but they are available also for external use.

**Code example**

    from bip_utils import P2PKH, P2SH, P2WPKH

    # P2PKH addresses (the default uses Bitcoin network address version, you can pass a different one as second parameter)
    addr = P2PKH.ToAddress(pub_key_bytes)
    # P2SH addresses (the default uses Bitcoin network address version, you can pass a different one as second parameter)
    addr = P2SH.ToAddress(pub_key_bytes)
    # P2WPKH addresses (the default uses Bitcoin network address version, you can pass a different one as second parameter)
    addr = P2WPKH.ToAddress(pub_key_bytes)

## WIF

This library is used internally by the other libraries, but it's available also for external use.

**Code example**

    import binascii
    from bip_utils import WifDecoder, WifEncoder

    key_bytes = binascii.unhexlify(b'1837c1be8e2995ec11cda2b066151be2cfb48adf9e47b151d46adab3a21cdf67')

    # Encode
    enc = WifEncoder.Encode(key_bytes)
    # Decode
    dec = WifDecoder.Decode(enc)

## Base58

This library is used internally by the other libraries, but it's available also for external use.
It supports both normal encode/decode and check_encode/check_decode.

**Code example**

    import binascii
    from bip_utils import Base58Decoder, Base58Encoder

    data_bytes = binascii.unhexlify(b"636363")

    # Normal encode
    enc     = Base58Encoder.Encode(data_bytes)
    # Check encode
    chk_enc = Base58Encoder.CheckEncode(data_bytes)

    # Normal decode
    dec     = Base58Decoder.Decode(enc)
    # Check decode, RuntimeError is raised if checksum verification fails
    chk_dec = Base58Decoder.CheckDecode(chk_enc)

## Bech32

This library is used internally by the other libraries, but it's available also for external use.

**Code example**

    import binascii
    from bip_utils import Bech32Decoder, Bech32Encoder

    data_bytes = binascii.unhexlify(b'9c90f934ea51fa0f6504177043e0908da6929983')

    # Encode
    enc = Bech32Encoder.EncodeAddr("bc", 0, data_bytes)
    # Decode
    dec = Bech32Decoder.DecodeAddr("bc", enc)

## Complete code example

Example from mnemonic generation to wallet addresses.

    from bip_utils import Bip39MnemonicGenerator, Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes

    # Generate random mnemonic
    mnemonic = Bip39MnemonicGenerator.FromWordsNumber(12)
    print("Mnemonic string: %s" % mnemonic)
    # Generate seed from mnemonic
    seed_bytes = Bip39SeedGenerator(mnemonic).Generate()

    # Generate BIP44 master keys
    bip_obj_mst = Bip44.FromSeed(seed_bytes, Bip44Coins.BITCOIN)
    # Print master key
    print("Master key (bytes): %s" % bip_obj_mst.PrivateKey().Raw().ToHex())
    print("Master key (extended): %s" % bip_obj_mst.PrivateKey().ToExtended())
    print("Master key (WIF): %s" % bip_obj_mst.PrivateKey().ToWif())

    # Generate BIP44 account keys: m/44'/0'/0'
    bip_obj_acc = bip_obj_mst.Purpose().Coin().Account(0)
    # Generate BIP44 chain keys: m/44'/0'/0'/0
    bip_obj_chain = bip_obj_acc.Change(Bip44Changes.CHAIN_EXT)

    # Generate the address pool (first 20 addresses): m/44'/0'/0'/0/i
    for i in range(20):
        bip_obj_addr = bip_obj_chain.AddressIndex(i)
        print("%d. Address public key (extended): %s" % (i, bip_obj_addr.PublicKey().ToExtended()))
        print("%d. Address private key (extended): %s" % (i, bip_obj_addr.PrivateKey().ToExtended()))
        print("%d. Address: %s" % (i, bip_obj_addr.PublicKey().ToAddress()))

# License

This software is available under the MIT license.
