using ERC20Mock as asset;

methods {
    function allowance(address, address) external returns uint256 envfree;
    function totalSupply() external returns uint256 envfree;
    function balanceOf(address) external returns uint256 envfree;
    function deposit(uint256, address) external returns (uint256);
    function redeem(uint256, address, address) external returns (uint256);
    function previewRedeem(uint256) external  returns (uint256) envfree;
    function previewDeposit(uint256 assets) external returns (uint256) envfree;


    function asset.balanceOf(address) external returns uint256 envfree;
    function asset.transfer(address, uint256) external returns (bool); 
}

/**
* Property 1: Property "Mint by user must increase totalSupply".
* Rule that proves users receive shares after calling mint()
*/
rule mintIncreasesTotalShareSupply(uint256 shares, address receiver) {
    env e;
    mathint total_supply_before = totalSupply();
    // number of user shares before minting
    mathint shares_before_mint = balanceOf(receiver);
    // this filters out states where the user's has more shares than the totalSupply as they should be unreachable, 
    // this should be proven to be true other rules
    require shares_before_mint <= to_mathint(totalSupply());

    // call the mint function in the contract
    mint(e, shares, receiver);

    // number of user shares after minting
    mathint shares_after_mint = balanceOf(receiver);
    // totalSupply of shares after minting
    mathint total_supply_after = totalSupply();

    // minting increases the totalSupply of shares in the system
    assert total_supply_after == total_supply_before + shares, "total supply should increase after minting";

    // asserting that the user's shares should increase after minting 
    assert shares_after_mint == shares_before_mint + shares, "user's shares after minting should increase";
}

/**
* Property 2: Property "Redeem by user must decrease totalSupply".
* Rule that proves that redemption decrease totalSupply of shares of the vault
*/
rule redeemDecreasesTotalShareSupply(uint256 shares, address receiver, address owner) {
    env e;
    require receiver != currentContract && owner != currentContract;
    
    mathint total_supply_before_redemption = totalSupply();
    // filters out unreachable states with shares greater than the totalSupply
    require total_supply_before_redemption >= to_mathint(shares);

    // proportional number of assets redeemed by share amount
    mathint redeemed_assets = previewRedeem(shares);
    mathint shares_before_redemption = balanceOf(owner);

    mathint receiver_asset_balance_before_redemption = asset.balanceOf(receiver);
    // protects against scenarios that cause overflow since transfer function uses unsafe addition to increment receiver's balance
    require receiver_asset_balance_before_redemption <= max_uint256 - redeemed_assets;

    redeem(e, shares, receiver, owner);

    mathint shares_after_redemption = balanceOf(owner);
    mathint total_supply_after_redemption = totalSupply();
    mathint receiver_asset_balance_after_redemption = asset.balanceOf(receiver);

    // assert that the totalSupply of shares should be decreased by redeemed amount of shares
    assert total_supply_after_redemption == total_supply_before_redemption - shares, "total supply of shares should be decreased by amount of redeemed shares";

    // asserting that the owner's shares should decrease by the redeemed amount of shares 
    assert shares_after_redemption == shares_before_redemption - shares, "owner's share balance should decrease";

    // receiver's balance should increase by an amount proportional to the shares redeemed
    assert receiver_asset_balance_after_redemption == receiver_asset_balance_before_redemption + redeemed_assets, "receiver's share balance should increase by redeemed amount of shares";
}
