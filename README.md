# ERC4626 Workshop Inflation Attack
Repository adapted from the Certora workshop on ERC4626 at TrustX @ Istanbul 2023.

The certora folder contains Certora CVL specification for the [inflation attack](https://tienshaoku.medium.com/eip-4626-inflation-sandwich-attack-deep-dive-and-how-to-solve-it-9e3e320cc3f1) on ERC4626 where the attack implemented in the specification aims to cover a more generalized version of the attack to make it more broadly applicable. 

The verification is checked against OpenZeppelin's [implementation of ERC4626](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/extensions/ERC4626.sol).

# Getting started

1. Familiarize yourself with the [ERC4626 specification](https://ethereum.org/en/developers/docs/standards/tokens/erc-4626/) and take a look at the (buggy) implementation of ERC4626 under `src`.
2. To get to know CVL take a look at the example specification under
[`certora/specs/Example.spec`](certora/specs/Example.spec).
3. Install the Certora prover ([Documentation](https://docs.certora.com/en/latest/docs/user-guide/getting-started/install.html#))
4. Run the InflationAttack specification by executing `certoraRun ERC4626_Workshop/certora/conf/Vault.conf` from within this folder to view the initial rules verified for the vault. Follow the link returned and wait for the verification to be completed. Alternatively, open the [pre-computed results](https://prover.certora.com/output/51488/9318516df38e44f3a3e53e992678e8b3/?anonymousKey=b427e6e78bef54690f6224e7ebd7ff4dcf4b7df4).
5. Run the Vault specification by executing `certoraRun ERC4626_Workshop/certora/conf/InflationAttack.conf` from within this folder to view the rule that verifies the inflation attack. Follow the link returned and wait for the verification to be completed. Alternatively, open the [pre-computed results](https://prover.certora.com/output/51488/2f4df3e9806d4a72828c678150c163cd/?anonymousKey=9fbbc0579ac75591c05d54d60408db01d33b4072).


# Additional Material

* [Prover Documentation](https://docs.certora.com/en/latest/)
* [ERC-4626 Specifications](https://ethereum.org/en/developers/docs/standards/tokens/erc-4626/)
* [Inflation Attack](https://tienshaoku.medium.com/eip-4626-inflation-sandwich-attack-deep-dive-and-how-to-solve-it-9e3e320cc3f1)


# About the CVL specs
The [specifications](InflationAttack/certora/spec/ERC4626-InflationAttack.spec) contain two rules. A CVL rule that step-by-step models inflation attack as described in the blog bost by 田少谷 Shao. But there is also a second rule, that is way simple but also detects the bug. 