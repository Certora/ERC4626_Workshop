using ERC20 as _ERC20;

methods {
    function _ERC20.balanceOf(address) external returns uint256 envfree;
    function allowance(address, address) external returns uint256 envfree;
    function balanceOf(address) external returns uint256 envfree;
    function previewWithdraw(uint256) external returns uint256 envfree;
    function previewRedeem(uint256) external returns uint256 envfree;
    function totalAssets() external returns uint256 envfree;
}

/**
* Special case where e.msg.sender == owner.
* 1. Third party `withdraw()` calls must update the msg.sender's allowance
* 2. withdraw() must allow proxies to withdraw tokens on behalf of the owner using share token approvals
* 3. Check that is doesn't revert. 
*/
rule ownerWithdrawal(uint256 assets, address receiver, address owner){
    env e; 
    require(e.msg.sender == owner);

    uint256 allowanceBefore = allowance(owner, e.msg.sender);
    withdraw@withrevert(e, assets, receiver, owner);
    uint256 allowanceAfter = allowance(owner, e.msg.sender);
    assert allowanceAfter == allowanceBefore;
    assert lastReverted == false;
}


/** 
* Third party `withdraw()` calls must update the msg.sender's allowance
* withdraw() must allow proxies to withdraw tokens on behalf of the owner using share token approvals
*/
rule thirdPartyWithdrawal(uint256 assets, address receiver, address owner){
    env e; 
    require(e.msg.sender != owner);

    uint256 allowanceBefore = allowance(owner, e.msg.sender);
    uint256 shares = previewWithdraw(assets);

    withdraw(e, assets, receiver, owner);

    uint256 allowanceAfter = allowance(owner, e.msg.sender);
    assert allowanceAfter <= allowanceBefore;
    assert shares <= allowanceBefore;
}


/** 
* Third party `withdraw()` calls must update the msg.sender's allowance
* withdraw() must allow proxies to withdraw tokens on behalf of the owner using share token approvals
*/
rule thirdPartyWithdrawal(uint256 assets, address receiver, address owner){
    env e; 
    require(e.msg.sender != owner);

    uint256 allowanceBefore = allowance(owner, e.msg.sender);
    uint256 shares = previewWithdraw(assets);

    withdraw(e, assets, receiver, owner);

    uint256 allowanceAfter = allowance(owner, e.msg.sender);
    assert allowanceAfter <= allowanceBefore;
    assert shares <= allowanceBefore;
}

/**
* Example of a parametric rule. 
*/
rule onlyOwnerCanIncreaseAllowance(method f, env e, calldataarg args, address owner){
    require(e.msg.sender != owner);

    uint256 allowanceBefore = allowance(owner, e.msg.sender);

    f(e,args);

    uint256 allowanceAfter = allowance(owner, e.msg.sender);
    assert allowanceAfter <= allowanceBefore;
}