<template>
    <!-- This will have two buttons a signup and login that goes to the corresponding views -->
    <h1>Main View</h1>
    <Button @click="gotoSignUpPage">Signup</Button>
    <Button @click="gotoLoginPage">Login</Button>
</template>

<script lang="ts">
    export default {
        methods : {
            gotoSignUpPage () {
                this.$router.push('/signup');
            },
            gotoLoginPage () {
                this.$router.push('/login');
            }
        }
    }
</script>