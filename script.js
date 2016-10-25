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
    console.log(user);
    writeData(user, token).then(signOut);
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

function writeData(user, token) {
  var data = {};

  data = {
    providerData: user.providerData,
    refreshToken: user.refreshToken,
    token: token
  };

  console.log(data);

  return firebase.database().ref('users/' + user.email.replace(".", "(dot)").replace("@", "(at)")).set(data).catch(e => console.log(e));
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
