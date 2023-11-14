using ERC20 as asset;

//Method block defining envfree method (and summaries)
methods {
    function totalSupply() external returns uint256 envfree;
    function balanceOf(address) external returns uint256 envfree;
    function allowance(address, address) external returns uint256 envfree;
    function totalAssets() external returns uint256 envfree;
    function asset.totalSupply() external returns uint256 envfree;
    function asset.balanceOf(address) external returns uint256 envfree;
    function asset.decimals() external returns uint8 envfree;
}

////////////////////////////////////////////////////////////////
//                                                            //
//            Simple Example Rules and Invariants             //
//                                                            //
////////////////////////////////////////////////////////////////

//Basic rule stating mint must increase totalAssets.
rule mintMustIncreaseTotalAssets(uint256 shares, address user){
    //State basic assumption that will be verified and hold.
    safeAssumptions();

    uint256 totalAssetsBefore = totalAssets();
    env e;
    mint(e, shares, user);
    uint256 totalAssetsAfter = totalAssets();
    assert totalAssetsAfter >= totalAssetsBefore, "Total assets must increase when mint is called."; 
}

//More complex rule stating a property on the relationship between totalSupply and totalAssets.
rule assetAndShareMonotonicity(env e, method f, uint256 amount, address receiver, address owner){
    safeAssumptions();
    uint256 totalAssetsBefore = totalAssets();
    uint256 totalSupplyBefore = totalSupply();
    
    //The assert only holds if the msg.sender isn't ERC4626 itself.
    require(e.msg.sender != currentContract);

    if(f.selector == sig:mint(uint,address).selector){
        mint(e, amount, receiver);
    } else if(f.selector == sig:withdraw(uint,address,address).selector){
        //The rule only holds if the receiver isn't ERC4626 itself!
        require(receiver != currentContract);
        withdraw(e, amount, receiver, owner);
    } else if(f.selector == sig:deposit(uint,address).selector){
        deposit(e, amount, receiver);
    } else if(f.selector == sig:redeem(uint,address,address).selector){
        //Commented out this necessary requirement on purpose. The rule fails.
        //require(receiver != currentContract);
        redeem(e, amount, receiver, owner);
    } else {
        calldataarg args;
        f(e,args);
    }
    
    uint256 totalAssetsAfter = totalAssets();
    uint256 totalSupplyAfter = totalSupply();

    assert totalSupplyBefore <= totalSupplyAfter <=> totalAssetsBefore <= totalAssetsAfter , "Monotonicity doesn't hold."; 
}

/*An example of an invariant: 
* An invariant is a property that holds before and after all method executions of a contract under verification.
*
* Invariant: When totalAssets of the underlying ERC20 vault (assets) is zero, totalSupply must be zero.
*/
invariant totalAssetsZeroImpliesTotalSupplyZero()
    totalAssets() == 0 => totalSupply() == 0
    {
        preserved {
            requireInvariant sumOfBalancesEqualsTotalSupplyERC4626;
            requireInvariant sumOfBalancesEqualsTotalSupplyERC20;
        }
}

//Invariant: When totalSupply is larger than zero, the underlying's ERC20 vault (asset) also must have a non-zero total balance.
invariant totalSupplyMatch()
    totalSupply() > 0 => asset.totalSupply() > 0
    {
        preserved {
            requireInvariant sumOfBalancesEqualsTotalSupplyERC20;
        }
    }


/*Safe assumptions below: These are invariants for the underyling ERC20 as well as ERC4626.
* The safeAssumptions use CVL features such as invariants, hooks and ghost.
*/
function safeAssumptions(){
    requireInvariant sumOfBalancesEqualsTotalSupplyERC4626;
    requireInvariant sumOfBalancesEqualsTotalSupplyERC20;
    requireInvariant singleUserBalanceSmallerThanTotalSupplyERC20;
    requireInvariant singleUserBalanceSmallerThanTotalSupplyERC4626;
}

////////////////////////////////////////////////////////////////
//                                                            //
//                       CVL Invariants                       //
//                                                            //
////////////////////////////////////////////////////////////////

invariant sumOfBalancesEqualsTotalSupplyERC4626()
    sumOfBalancesERC4626 == to_mathint(totalSupply());

invariant sumOfBalancesEqualsTotalSupplyERC20()
    sumOfBalancesERC20 == to_mathint(asset.totalSupply());

invariant singleUserBalanceSmallerThanTotalSupplyERC20()
    userBalanceERC20 <= sumOfBalancesERC20;

invariant singleUserBalanceSmallerThanTotalSupplyERC4626()
    userBalanceERC4626 <= sumOfBalancesERC4626;

////////////////////////////////////////////////////////////////
//                                                            //
//                      Ghost Variables                       //
//                                                            //
////////////////////////////////////////////////////////////////
//A ghost is a state variable of CVL that can be modified, for instance, in hooks. 

//Ghost variable tracking the total sum of all balances of ERC4626
ghost mathint sumOfBalancesERC4626 {
    init_state axiom sumOfBalancesERC4626 == 0;
}

ghost mathint sumOfBalancesERC20 {
    init_state axiom sumOfBalancesERC20 == 0;
}

ghost mathint userBalanceERC20 {
    init_state axiom userBalanceERC20 == 0;
}

//Ghost variable tracking a "ghost" mapping of the balances of all addresses
ghost mapping(address => uint256) balanceOfMirroredERC4626 {
    init_state axiom forall address a. (balanceOfMirroredERC4626[a] == 0);
}

ghost mapping(address => uint256) balanceOfMirroredERC20 {
    init_state axiom forall address a. (balanceOfMirroredERC20[a] == 0);
}

ghost mathint userBalanceERC4626 {
    init_state axiom userBalanceERC4626 == 0;
}

////////////////////////////////////////////////////////////////
//                                                            //
//                         CVL Hooks                          //
//                                                            //
////////////////////////////////////////////////////////////////
//Hooks intercept EVM instructions and allows adding custom logic. 

//A store hook that triggers on every store to the storage variable `balanceOf` of ERC4626 (currentContract).
hook Sstore currentContract.balanceOf[KEY address user] uint256 newValue (uint256 oldValue) STORAGE {
    //Updating the ghost variable sumOfBalances
    sumOfBalancesERC4626 = sumOfBalancesERC4626 + newValue - oldValue;
    //Also updating a second ghost variable.
    userBalanceERC4626 = newValue;
    balanceOfMirroredERC4626[user] = newValue;
}

//A store hook that triggers on every store to the storage variable `balanceOf` of ERC20.
hook Sstore asset.balanceOf[KEY address user] uint256 newValue (uint256 oldValue) STORAGE {
    sumOfBalancesERC20 = sumOfBalancesERC20 + newValue - oldValue;
    userBalanceERC20 = newValue;
    balanceOfMirroredERC20[user] = newValue;
}

//A load hook that triggers on every load from the storage variable `balanceOf` of ERC20.
hook Sload uint256 value currentContract.balanceOf[KEY address user] STORAGE {
    require to_mathint(value) <= sumOfBalancesERC4626;
    require value == balanceOfMirroredERC4626[user];
}

//A load hook that triggers on every load from the storage variable `balanceOf` of ERC20.
hook Sload uint256 value asset.balanceOf[KEY address user] STORAGE {
    require to_mathint(value) <= sumOfBalancesERC20;
    require value == balanceOfMirroredERC20[user];
}
