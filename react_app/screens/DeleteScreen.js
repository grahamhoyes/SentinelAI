import React from 'react';
import {
  Image,
  Platform,
  ScrollView,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
  Button,
  Alert,
  encodedURIComponent,
  TextInput,
  navigate
} from 'react-native';

import { WebBrowser } from 'expo';
import { MonoText } from '../components/StyledText';


export default class RegisterScreen extends React.Component {
  // header has go back arrow
  constructor(props) {
    super(props);
    this.state = { delete_person: "" };
    this._register = this._register.bind(this);
  }

  _register(){
    fetch(`https://sentinelai.mybluemix.net/request?name=${ this.state.delete_person }&delete=true`, { method: 'GET' });
    global.registered_people.splice( global.registered_people.indexOf(this.state.delete_person), 1);
    Alert.alert(this.state.delete_person + " has been deleted.")
  }

  render() {
    const { navigate } = this.props.navigation
    return (
      <View style={styles.container}>
        <ScrollView style={styles.container} contentContainerStyle={styles.contentContainer}>
          <View style={styles.welcomeContainer}>
            <Image
              source={
                __DEV__
                  ? require('../assets/images/sentinelAI.png')
                  : require('../assets/images/sentinelAI.png')
              }
              style={styles.welcomeImage}
            />
          </View>

          <View style={styles.textContainer}>
            <Text style={styles.generalText}>Name: </Text>
            <TextInput
              style={{height: 40}}
              placeholder="Please input the name of the user you wish to delete"
              onChangeText={(delete_person) => this.setState({delete_person})}
            />
          </View>

          <View style={styles.textContainer}>
            <Button onPress={this._register} title="Delete User" color="#94e087"/>
          </View>
        </ScrollView>

        <View style={styles.tabBarInfoContainer}>
          <Text style={styles.tabBarInfoText}>Note: This is a beta version of SentinelAI</Text>
        </View>
      </View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 19, 
    fontWeight: 'bold'
  },
  developmentModeText: {
    marginBottom: 20,
    color: 'rgba(0,0,0,0.4)',
    fontSize: 14,
    lineHeight: 19,
    textAlign: 'center',
  },
  contentContainer: {
    paddingTop: 30,
  },
  textContainer: {
    paddingTop: 30,
    marginHorizontal: 40,
  },
  welcomeContainer: {
    alignItems: 'center',
    marginTop: 10,
    marginBottom: 20,
  },
  welcomeImage: {
    width: 100,
    height: 80,
    resizeMode: 'contain',
    marginTop: 30,
    marginLeft: -10,
  },
  getStartedContainer: {
    alignItems: 'center',
    marginHorizontal: 50,
  },
  homeScreenFilename: {
    marginVertical: 7,
  },
  codeHighlightText: {
    color: 'rgba(96,100,109, 0.8)',
  },
  codeHighlightContainer: {
    backgroundColor: 'rgba(0,0,0,0.05)',
    borderRadius: 3,
    paddingHorizontal: 4,
  },
  getStartedText: {
    fontSize: 17,
    color: 'rgba(96,100,109, 1)',
    lineHeight: 24,
    textAlign: 'center',
  },
  generalText:{
    fontSize: 14,
    color: 'rgba(96,100,109, 1)',
    lineHeight: 24
  },
  tabBarInfoContainer: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    ...Platform.select({
      ios: {
        shadowColor: 'black',
        shadowOffset: { height: -3 },
        shadowOpacity: 0.1,
        shadowRadius: 3,
      },
      android: {
        elevation: 20,
      },
    }),
    alignItems: 'center',
    backgroundColor: '#fbfbfb',
    paddingVertical: 20,
  },
  tabBarInfoText: {
    fontSize: 12,
    color: 'rgba(96,100,109, 1)'
  },
  navigationFilename: {
    marginTop: 5,
  },
  helpContainer: {
    marginTop: 15,
    alignItems: 'center',
  },
  helpLink: {
    paddingVertical: 15,
  },
  helpLinkText: {
    fontSize: 14,
    color: '#2e78b7',
  },
});
