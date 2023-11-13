using ERC20 as asset;

methods {
    function allowance(address, address) external returns uint256 envfree;
    function previewWithdraw(uint256) external returns uint256 envfree;
    function totalAssets() external returns uint256 envfree;
    function totalSupply() external returns uint256 envfree;
    function asset.totalSupply() external returns uint256 envfree;
}

/**
* Property 1: Property "Withdrawal by the owner doesnt change allowance".
* Write a rule that proves that withdrawal doesn't change allowance, 
* in the case that the message sender is the owner of the funds.
*/
rule withdrawalByOwnerHasNoImpactOnAllowance(uint256 assets, address receiver, address owner){
    env e; 
    require(e.msg.sender == owner);

    //Implement task here
}


/**
* Property 2: "Withdrawal by third party changes allowance".
* Write a rule that proves that withdrawal changes allowance, 
* in the case that the message sender is _NOT_ the owner of the funds.
* 
* How can allowance change in this case? Can it increase or decrease? Prove it! 
*/
rule withdrawlByThirdPartyDecreasesAllowance(uint256 assets, address receiver, address owner){
    env e; 
    require(e.msg.sender != owner);

    //Implement task here
}

/**
* Property 3: Only methods X changes allowance when the msg.sender is not the owner. 
* Task 1: Find the set of methods X that can change the allowance value.
* Task 2: What happens if you remove the statement require(e.msg.sender != owner);?
*/
rule onlyOwnerCanIncreaseAllowance(method f, env e, calldataarg args, address owner){
    require(e.msg.sender != owner);

    //Implement task here
}