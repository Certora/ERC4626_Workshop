# ERC4626 Workshop
Repository alongside the Certora workshop on ERC4626 at TrustX @ Istanbul 2023.

# Getting started

1. Familiarize yourself with the [ERC4626 specification](https://ethereum.org/en/developers/docs/standards/tokens/erc-4626/) and take a look at the (buggy) implementation of ERC4626 under `src`.
2. To get to know CVL take a look at the example specification under
[`certora/specs/Example.spec`](certora/specs/Example.spec).
3. Install the Certora prover ([Documentation](https://docs.certora.com/en/latest/docs/user-guide/getting-started/install.html#))
4. Run the specification by executing `certoraRun certora/specs/Example.spec` from within this folder. Follow the link returned and wait for the verification to be completed. Alternatively, open the [pre-computed results](https://prover.certora.com/output/53900/e34b40742baa466b9d35827d2d8a8a64/?anonymousKey=2bccddcb7834b2f79b4315a79f2e52a0118aad7a).
5. Inspect the results and make yourself familiar with the output. 
_Note: The rule `assetAndShareMonotonicity` is failing as of a bug in the code. (Inflation Attack)_
6. Think about properties of ERC4626 and note them down in https://docs.google.com/document/d/116HDhYT8pJMD9DOdrS8NdWdvTnOdsIcEQK9AjnxpdnY/edit

# Write your own CVL specifications

1. Open the file `certora/specs/Tutorial.spec`. 
2. The file contains three rule signatures that need to be implemented. Take a look at the comment and write the specifications.
3. The solutions are found in branch `solutions`.
4. On branch `solutions` there is a [`Properties.md`](Properties.m) file that lists basic properties for ERC4626. Enhance your CVL specifications to also cover those properties. Which ones can you prove?


# Additional Material

* [Prover Documentation](https://docs.certora.com/en/latest/)
* [ERC-4626 Specifications](https://ethereum.org/en/developers/docs/standards/tokens/erc-4626/)
* [Inflation Attack](https://tienshaoku.medium.com/eip-4626-inflation-sandwich-attack-deep-dive-and-how-to-solve-it-9e3e320cc3f1)