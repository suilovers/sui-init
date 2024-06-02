module test33::test33_tests {
    // uncomment this line to import the module
    // use test33::test33;

    const ENotImplemented: u64 = 0;

    #[test]
    fun test_test33() {
        // pass
    }

    #[test, expected_failure(abort_code = ::test33::test33_tests::ENotImplemented)]
    fun test_test33_fail() {
        abort ENotImplemented
    }
}
