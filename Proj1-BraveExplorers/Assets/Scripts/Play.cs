using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class Play : MonoBehaviour {

	public enum Status {Placing, Playing};
	public Button startButton;
	public Button quitButton;
	public Button okButton;
	public Button deathOkButton;
	public Status status;
	public Timer time;
	public GameObject readyButton;
	public GameObject leftButton;
	public GameObject rightButton;
	public GameObject pauseButton;
	public GameObject jumpButton;
	public GameObject undoButton;
	public GameObject lockButton;
	public GameObject blue;
	public GameObject timer;
	public GameObject gameEnd;
	public GameObject exitWarning;
	public GameObject deathWindow;

	public GameObject chaiseLong;
	public GameObject books;
	public GameObject trap;
	public GameObject basketball;
	public GameObject exit;

	public Text endText;

	// Use this for initialization
	void Start () {
		
		toggleOriginals(true);

		status = Status.Placing;
		startButton.onClick.AddListener(StartGame);
		quitButton.onClick.AddListener(time.Quit);
		deathOkButton.onClick.AddListener(time.Quit);
		okButton.onClick.AddListener(Ok);

		leftButton.SetActive(false);
		rightButton.SetActive(false);
		jumpButton.SetActive(false);
		pauseButton.SetActive(false);
		blue.SetActive(false);
		timer.SetActive(false);
		gameEnd.SetActive(false);
		exitWarning.SetActive(false);
		deathWindow.SetActive(false);

	}

	public void StartGame(){

		if (!checkForExit()){
			exitWarning.SetActive(true);
			return;
		}

		toggleOriginals(false);

		this.status = Status.Playing;

		leftButton.SetActive(true);
		rightButton.SetActive(true);
		jumpButton.SetActive(true);
		pauseButton.SetActive(true);
		blue.SetActive(true);
		timer.SetActive(true);

		undoButton.SetActive(false);
		readyButton.SetActive(false);
		lockButton.SetActive(false);

		time.StartTimer();		
	}

	public void EndLevel(){
		endText.text = time.EndTimer();
		timer.SetActive(false);
		blue.SetActive(false);
		pauseButton.SetActive(false);
		leftButton.SetActive(false);
		rightButton.SetActive(false);
		jumpButton.SetActive(false);
		gameEnd.SetActive(true);
	}

	public bool checkForExit(){
		if (GameObject.Find("fireexitdoor Container") != null) return true;
		return false;
	}

	public void Ok(){
		exitWarning.SetActive(false);
	}

	public void Die(){
		deathWindow.SetActive(true);
	}

	void toggleOriginals(bool val){
		chaiseLong.SetActive(val);
		books.SetActive(val);
		trap.SetActive(val);
		basketball.SetActive(val);
		exit.SetActive(val);
	}

}
