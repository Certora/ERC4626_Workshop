

using ERC20Mock as asset;

methods{
    function balanceOf(address) external returns uint256 envfree;
    function deposit(uint256, address) external returns (uint256);
    function redeem(uint256, address, address) external returns (uint256);
    function maxRedeem(address owner) external returns (uint256) envfree;

    function asset.balanceOf(address) external returns uint256 envfree;
} 

rule shareInflationAttack(uint256 assets, address deposit_receiver, address redeem_receiver, address redeem_owner) {
    env e;
    address attacker = e.msg.sender;

    require(balanceOf(attacker) == 0);
    require(balanceOf(deposit_receiver) == 0);
    require(balanceOf(redeem_receiver) == 0);
    require(balanceOf(redeem_owner) == 0);

    require(attacker != currentContract);

    uint256 shares = deposit(e, assets, deposit_receiver);

    // asset balance of the Vault contract for illustrative purposes
    uint256 vault_asset_balance = asset.balanceOf(currentContract);

    uint256 receivedAssets = redeem(e, shares, redeem_receiver, redeem_owner);

    assert receivedAssets <= assets, "The attacker gained assets.";
} 
