export const initialValue = `module MyModule {
    use 0x1::Coin;
    use 0x1::Signer;
    
    struct MyStruct has copy, drop {
        value: u64,
    }
    
    public fun my_function(account: &signer) {
        let x = 10;
        let y = 20;
        let result = x + y;
        let my_struct = MyStruct { value: result };
        Coin::deposit(account, my_struct.value);
        return my_struct;
    }
    
    public fun another_function() {
        let condition = true;
        if (condition) {
            return 1;
        } else {
            return 0;
        }
    }
    }`;