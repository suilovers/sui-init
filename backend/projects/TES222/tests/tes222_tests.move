module tes222::tes222_tests {
    // uncomment this line to import the module
    // use tes222::tes222;

    const ENotImplemented: u64 = 0;

    #[test]
    fun test_tes222() {
        // pass
    }

    #[test, expected_failure(abort_code = ::tes222::tes222_tests::ENotImplemented)]
    fun test_tes222_fail() {
        abort ENotImplemented
    }adsad
}asdad