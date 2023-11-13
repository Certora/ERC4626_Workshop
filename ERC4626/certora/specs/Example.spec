using ERC20 as _ERC20;

//Method block defining envfree method (and summaries)
methods {
    function totalSupply() external returns uint256 envfree;
    function balanceOf(address) external returns uint256 envfree;
    function allowance(address, address) external returns uint256 envfree;
    function totalAssets() external returns uint256 envfree;
    function previewMint(uint256) external returns uint256 envfree;
    function previewWithdraw(uint256) external returns uint256 envfree;
    function previewDeposit(uint256) external returns uint256 envfree;
    function previewRedeem(uint256) external returns uint256 envfree;
    function convertToShares(uint256) external returns uint256 envfree;
    function _ERC20.totalSupply() external returns uint256 envfree;
    function _ERC20.balanceOf(address) external returns uint256 envfree;
}

rule convertToSharesIsAdditive(uint256 assetX, uint256 assetY){
    
    uint256 sharesX = convertToShares(assetX);
    uint256 sharesY = convertToShares(assetY);

    //Ensure no overflow is occuring.
    uint256 sumOfAssets = require_uint256(assetX + assetY);
    uint256 sharesOfSumOfAssets = convertToShares(sumOfAssets);

    //Assert  no overflow is occuring.
    assert sharesOfSumOfAssets <= require_uint256(assetX + sharesY), "convertToShares is not additive.";
}


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

    if(f.selector == sig:mint(uint,address).selector){
        mint(e, amount, receiver);
    } else if(f.selector == sig:withdraw(uint,address,address).selector){
        withdraw(e, amount, receiver, owner);
    } else if(f.selector == sig:deposit(uint,address).selector){
        deposit(e, amount, receiver);
    } else if(f.selector == sig:redeem(uint,address,address).selector){
        redeem(e, amount, receiver, owner);
    } else {
        calldataarg args;
        f(e,args);
    }
    
    uint256 totalAssetsAfter = totalAssets();
    uint256 totalSupplyAfter = totalSupply();

    require(e.msg.sender != currentContract);
    assert totalSupplyBefore <= totalSupplyAfter <=> totalAssetsBefore <= totalAssetsAfter , "Monotonicity doesn't hold."; 
}



/*Safe assumptions below: These are invariants for the underyling ERC20 as well as ERC4626.
* The safeAssumptions use CVL features such as invariant, hooks and ghost.
*/
function safeAssumptions(){
    requireInvariant sumOfBalancesEqualsTotalSupplyERC4626;
    requireInvariant sumOfBalancesEqualsTotalSupplyERC20;
    requireInvariant singleUserBalanceSmallerThanTotalSupplyERC20;
    requireInvariant singleUserBalanceSmallerThanTotalSupplyERC4626;
}

function balaceMirrorsAreCorrect(address x) {
    requireInvariant mirrorIsCorrectERC20(x);
    requireInvariant mirrorIsCorrectERC4626(x);
}

function safeAssumptionsERC20() {
    requireInvariant sumOfBalancesEqualsTotalSupplyERC20;
    requireInvariant singleUserBalanceSmallerThanTotalSupplyERC20;
}


invariant totalAssetsZeroImpliesTotalSupplyZero()
    totalAssets() == 0 => totalSupply() == 0
    {

        preserved {
            requireInvariant sumOfBalancesEqualsTotalSupplyERC4626;
            requireInvariant sumOfBalancesEqualsTotalSupplyERC20;
            requireInvariant singleUserBalanceSmallerThanTotalSupplyERC4626;
            requireInvariant singleUserBalanceSmallerThanTotalSupplyERC20;
        }
}

//An invariant is a property that holds before and after all method executions of a contract under verification.
invariant sumOfBalancesEqualsTotalSupplyERC4626()
    sumOfBalancesERC4626 == to_mathint(totalSupply());

//A ghost is a state variable of CVL that can be modified, for instance, in hooks. 
ghost mathint sumOfBalancesERC4626 {
    init_state axiom sumOfBalancesERC4626 == 0;
}

//Hooks are a way to track changes to 
hook Sstore currentContract.balanceOf[KEY address user] uint256 newValue (uint256 oldValue) STORAGE {
    sumOfBalancesERC4626 = sumOfBalancesERC4626 + newValue - oldValue;
    userBalanceERC4626 = newValue;
    balanceOfMirroredERC4626[user] = newValue;
}

hook Sload uint256 value currentContract.balanceOf[KEY address user] STORAGE {
    require to_mathint(value) <= sumOfBalancesERC4626;
    require value == balanceOfMirroredERC4626[user];
}

invariant sumOfBalancesEqualsTotalSupplyERC20()
    sumOfBalancesERC20 == to_mathint(_ERC20.totalSupply());

ghost mathint sumOfBalancesERC20 {
    init_state axiom sumOfBalancesERC20 == 0;
}

hook Sstore _ERC20.balanceOf[KEY address user] uint256 newValue (uint256 oldValue) STORAGE {
    sumOfBalancesERC20 = sumOfBalancesERC20 + newValue - oldValue;
    userBalanceERC20 = newValue;
    balanceOfMirroredERC20[user] = newValue;
}

hook Sload uint256 value _ERC20.balanceOf[KEY address user] STORAGE {
    //This line makes the proof work. But is this actually safe to assume? With every load in the programm, we assume the invariant to already hold.
    require to_mathint(value) <= sumOfBalancesERC20;
    require value == balanceOfMirroredERC20[user];
}

invariant singleUserBalanceSmallerThanTotalSupplyERC20()
    userBalanceERC20 <= sumOfBalancesERC20;

ghost mathint userBalanceERC20 {
    init_state axiom userBalanceERC20 == 0;
}

invariant singleUserBalanceSmallerThanTotalSupplyERC4626()
    userBalanceERC4626 <= sumOfBalancesERC4626;

ghost mathint userBalanceERC4626 {
    init_state axiom userBalanceERC4626 == 0;
}

ghost mapping(address => uint256) balanceOfMirroredERC4626 {
    init_state axiom forall address a. (balanceOfMirroredERC4626[a] == 0);
}

ghost mapping(address => uint256) balanceOfMirroredERC20 {
    init_state axiom forall address a. (balanceOfMirroredERC20[a] == 0);
}

invariant mirrorIsCorrectERC20(address x)
    balanceOfMirroredERC20[x] == _ERC20.balanceOf(x);


invariant mirrorIsCorrectERC4626(address x)
    balanceOfMirroredERC4626[x] == balanceOf(x);