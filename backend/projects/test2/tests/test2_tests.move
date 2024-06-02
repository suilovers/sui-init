module test2::test2_tests {
    // uncomment this line to import the module
    // use test2::test2;

    const ENotImplemented: u64 = 0;

    #[test]
    fun test_test2() {
        // pass
    }

    #[test, expected_failure(abort_code = ::test2::test2_tests::ENotImplemented)]
    fun test_test2_fail() {
        abort ENotImplemented
    }
}
