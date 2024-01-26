<script>
  window.onSignIn = (googleUser) => {
     const profile = googleUser.getBasicProfile();
     console.log('ID: ' + profile.getId());
     console.log('Name: ' + profile.getName());
     console.log('Image URL: ' + profile.getImageUrl());
     console.log('Email: ' + profile.getEmail());
  };
</script>

<svelte:head>
  <script src="https://apis.google.com/js/platform.js?onload=onLoadCallback" async defer></script>
</svelte:head>

<div class="g-signin2" data-longtitle="true" data-onsuccess="onSignIn" />

<!-- Whack this somewhere? -->
<!--<script>-->
<!--  let userLoggedIn = false;-->
<!--  window.onLoadCallback = () => {-->
<!--    userLoggedIn = gapi.auth2.getAuthInstance().isSignedIn.get();-->
<!--    if (userLoggedIn) {  -->
<!--      // Handle login-->
<!--    }-->
<!--  }-->
<!--</script>-->