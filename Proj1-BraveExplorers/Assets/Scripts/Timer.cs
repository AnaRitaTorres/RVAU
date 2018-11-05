using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class Timer : MonoBehaviour {

	public Text timerText;
	public Button pauseButton;
	public Button continueButton;
	public Button quitButton;
	public GameObject backgroundWindow;
	public GameObject dialogWindow;
	private float startTime;
	private bool pause = false;
	private bool menu = false;
	private float pausedAt;
	private float t;

	void Start() {
		backgroundWindow.SetActive(false);
		dialogWindow.SetActive(false);
		startTime = Time.time;
		pauseButton.onClick.AddListener(Pause);
		continueButton.onClick.AddListener(Continue);
		quitButton.onClick.AddListener(Quit);
	}
	
	void Update() {

		if(!pause) {
			t = Time.time - startTime;
			string minutes = ((int) t/60).ToString("f1");
			string seconds = (t % 60).ToString("f1");
			timerText.text = "00:" + minutes + ":" + seconds;
		}
	}

	void Pause() {

		if(pause) {
			pause = false;
			t = pausedAt;
		}
		else {
			pause = true; 
			pausedAt = Time.time;
			backgroundWindow.SetActive(true);
			dialogWindow.SetActive(true);
			menu = true;
		}
	}

	void Continue() {
		if(menu) {
			backgroundWindow.SetActive(false);
			dialogWindow.SetActive(false);
			pause = false;
			pausedAt = Time.time;
			menu = false;
		}
	}

	void Quit() {
		Debug.Log("Outtt");
		Application.Quit();
	}
}
