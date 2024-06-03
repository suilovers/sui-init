module demo2::demo2_tests {
    // uncomment this line to import the module
    // use demo2::demo2;

    const ENotImplemented: u64 = 0;

    #[test]
    fun test_demo2() {
        // pass
    }

    #[test, expected_failure(abort_code = ::demo2::demo2_tests::ENotImplemented)]
    fun test_demo2_fail() {
        abort ENotImplemented
    }
}
