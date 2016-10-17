'use strict';

// Initialize Firebase
var config = {
  apiKey: "AIzaSyApIfwmmhA0GZemplwVIxcBeScByYXuvsU",
  authDomain: "ember-ai-146020.firebaseapp.com",
  databaseURL: "https://ember-ai-146020.firebaseio.com",
  storageBucket: "ember-ai-146020.appspot.com",
  messagingSenderId: "295894273459"
};
firebase.initializeApp(config);

document.getElementById("signup").addEventListener("click", signUp);

function signUp() {
  var provider = new firebase.auth.GoogleAuthProvider();

  provider.addScope('https://www.googleapis.com/auth/calendar');

  firebase.auth().signInWithPopup(provider).then(function(result) {
    // This gives you a Google Access Token. You can use it to access the Google API.
    var token = result.credential.accessToken;
    // The signed-in user info.
    var user = result.user;
    signOut();
    // ...
  }).catch(function(error) {
    // Handle Errors here.
    var errorCode = error.code;
    var errorMessage = error.message;
    // The email of the user's account used.
    var email = error.email;
    // The firebase.auth.AuthCredential type that was used.
    var credential = error.credential;
    // ...
  });
}

function signOut() {
  firebase.auth().signOut().then(function() {
    // Sign-out successful.
    console.log("User signed out")
  }, function(error) {
    // An error happened.
    console.log("Sign out failed");
  });
}
