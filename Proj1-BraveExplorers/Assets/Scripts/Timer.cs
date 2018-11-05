using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class Timer : MonoBehaviour {

	public Text timerText;
	public Button pauseButton;
	private float startTime;
	private bool pause = false;
	private float pausedAt;
	private float t;

	void Start() {
		
		startTime = Time.time;
		pauseButton.onClick.AddListener(Pause);
	}
	
	void Update() {

		if(!pause) {
			t = Time.time - startTime;
			string minutes = ((int) t/60).ToString("f1");
			string seconds = (t % 60).ToString("f1");
			Debug.Log(t%60);
			timerText.text = "00:" + minutes + ":" + seconds;
		}
	}

	void Pause() {

		if(pause){
			pause = false;
			t = pausedAt;
			Update();
		}
		else {
			pause = true;
			pausedAt = Time.time;
		}
	}
}
