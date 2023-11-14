

using ERC20Mock as asset;

methods{
    function asset.allowance(address,address) external returns uint256 envfree;
    function asset.balanceOf(address) external returns uint256 envfree;
    function asset.decimals() external returns uint8 envfree;
    function asset.totalSupply() external returns uint256 envfree;
    
    function balanceOf(address) external returns uint256 envfree;
    function convertToAssets(uint256) external returns uint256 envfree;
    function convertToShares(uint256) external returns uint256 envfree;
    function decimals() external returns uint8 envfree;
    function previewDeposit(uint256) external returns uint256 envfree;
    function previewMint(uint256) external returns uint256 envfree;
    function previewWithdraw(uint256) external returns uint256 envfree;
    function totalAssets() external returns uint256 envfree;
    function totalSupply() external returns uint256 envfree;

    function Math.mulDiv(uint256 x, uint256 y, uint256 denominator) internal returns uint256 => mulDivSummary(x,y,denominator);
} 

function mulDivSummary(uint256 x, uint256 y, uint256 denominator) returns uint256 {
    return require_uint256(x*y/denominator);
}


rule simpleVersionOfInflationAttack(uint256 assets, address deposit_receiver, address redeem_receiver, address redeem_owner) {
    env e;
    address attacker = e.msg.sender;

    require(balanceOf(attacker) == 0);
    require(balanceOf(deposit_receiver) == 0);
    require(balanceOf(redeem_receiver) == 0);
    require(balanceOf(redeem_owner) == 0);

    require(attacker != currentContract);

    uint256 shares = deposit(e, assets, deposit_receiver);
    uint256 receivedAssets = redeem(e, shares, redeem_receiver, redeem_owner);

    assert receivedAssets <= assets, "The attacker gained assets.";
}

//Source: Medium Article by Shao https://tienshaoku.medium.com/eip-4626-inflation-sandwich-attack-deep-dive-and-how-to-solve-it-9e3e320cc3f1
rule complexVersionOfInflationAttack(address attacker, address victim, address deposit1_receiver, address deposit2_victim_receiver,address redeem_receiver,address redeem_owner ){
    uint256 amountToDeposit;
    uint256 amountDirectTransferToUnderlying;

    require(amountToDeposit > 0);
    require(amountDirectTransferToUnderlying > 0);

    mathint assetsAttackerPreAttack = to_mathint(amountToDeposit) + to_mathint(amountDirectTransferToUnderlying);
    
    //Excluding cases of counter example that are not of interest.
    require(attacker != currentContract);
    require(attacker != asset);
    require(attacker != 0);
    require(victim != currentContract);
    require(victim != asset);
    require(victim != 0);
    require(victim != attacker);

    //Following the pattern "First Deposit" of the article.
    require(totalSupply() == 0);
    require(totalAssets() == 0);

    //Duplicated all requireInvariants
    require(balanceOf(attacker) == 0);
    require(balanceOf(victim) == 0);
    require(balanceOf(deposit1_receiver) == 0);
    require(balanceOf(deposit2_victim_receiver) == 0);
    require(balanceOf(redeem_receiver) == 0);
    require(balanceOf(redeem_owner) == 0);

    //These are fair assumptions on the addresses, the attacker can control these addresses
    require(attacker == deposit1_receiver);
    require(attacker == redeem_owner);
    require(attacker == redeem_receiver);

    //It is important that deposit2_victim_receiver is not equal to attacker, as otherwise the deposit by the victim has to transfer assets to the attacker. 
    //This would mean the victim already trusts the attacker. Interstingly, we could find a CEX for this case as well. 
    require(deposit2_victim_receiver != attacker);

    //Manually ensuring sumOfBalances <= totalSupply() for underyling vault + ERC4626 vault
    require(balanceOf(attacker) + balanceOf(victim) + balanceOf(deposit1_receiver) + balanceOf(deposit2_victim_receiver) + balanceOf(redeem_receiver) + balanceOf(redeem_owner) <= to_mathint(totalSupply()));
    require(asset.balanceOf(currentContract) + asset.balanceOf(attacker) + asset.balanceOf(victim) + asset.balanceOf(deposit1_receiver) +asset.balanceOf(deposit2_victim_receiver) +asset.balanceOf(redeem_receiver) + asset.balanceOf(redeem_owner) <= to_mathint(asset.totalSupply()));
        
    uint256 before_step_1_totalSupply = totalSupply();
    uint256 before_step_1_totalAssets = totalAssets();

    /**
    * Step 1: the attacker front-runs the depositor and deposits 1 wei WETH and gets 1 share: since totalSupply is 0, shares = 1 * 10**18 / 10**18 = 1
    */
    env e1;
    require(e1.msg.sender == attacker);
    uint256 firstShares = deposit(e1, amountToDeposit, deposit1_receiver);
    
    uint256 before_step_2_totalSupply = totalSupply();
    uint256 before_step_2_totalAssets = totalAssets();

    env e2;
    require(e2.msg.sender == attacker);
    require(e2.block.timestamp > e1.block.timestamp);

    require(asset.balanceOf(attacker) >= amountDirectTransferToUnderlying);

    /**
    * Step 2: the attacker also transfers 1 * 1e18 weiWETH, making the totalAssets() WETH balance of the vault become 1e18 + 1 wei
    */
    asset.transferFrom(e2, attacker, currentContract, amountDirectTransferToUnderlying);
    require(asset.balanceOf(currentContract) > 0);
    
    uint256 before_step_3_totalSupply = totalSupply();
    uint256 before_step_3_totalAssets = totalAssets();
    
    /** 
    * Step 3: 
    * The spied-on depositor deposits 1e18 wei WETH. However, the depositor gets 0 shares: 1e18 * 1 (totalSupply) / (1e18 + 1) = 1e18 / (1e18 + 1) = 0. 
    * Since the depositor gets 0 shares, totalSupply() remains at 1
    */
    env e3;
    require(e3.msg.sender == victim);
    require(e3.block.timestamp > e2.block.timestamp);
    uint256 previweAssets = previewDeposit(amountDirectTransferToUnderlying);
    uint256 victimShares = deposit(e3, amountDirectTransferToUnderlying, deposit2_victim_receiver);
    
    /**
    * Step 4: the attacker still has the 1 only share ever minted and thus the withdrawal of
    * that 1 share takes away everything in the vault, including the depositor’s 1e18 weiWETH
    */
    
    uint256 before_step_4_totalSupply = totalSupply();
    uint256 before_step_4_totalAssets = totalAssets();

    env e4;
    require(e4.msg.sender == attacker);
    require(e4.block.timestamp > e3.block.timestamp);
    mathint assetsAttackerPostAttack = redeem(e4, before_step_4_totalSupply, redeem_receiver, redeem_owner);

    uint256 finalTotalAssets = totalAssets();
    uint256 finalTotalSupply = totalSupply();
    mathint assetsAttackerGained = assetsAttackerPostAttack - assetsAttackerPreAttack;
    
    assert assetsAttackerPreAttack >= assetsAttackerPostAttack, "The attacker gained assets.";
}
