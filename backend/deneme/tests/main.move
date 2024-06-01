script {
    use 0x1::MyModule;

    fun test_hello_world() {
        MyModule::hello_world();
    }
}