module test222::test222_tests {
    // uncomment this line to import the module
    // use test222::test222;

    const ENotImplemented: u64 = 0;

    #[test]
    fun test_test222() {
        // pass
    }

    #[test, expected_failure(abort_code = ::test222::test222_tests::ENotImplemented)]
    fun test_test222_fail() {
        abort ENotImplemented
    }
}
