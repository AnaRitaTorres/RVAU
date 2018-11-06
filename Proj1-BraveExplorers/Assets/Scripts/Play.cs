using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class Play : MonoBehaviour {

	public enum Status {Placing, Playing};
	public Button startButton;
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

	// Use this for initialization
	void Start () {
		status = Status.Placing;
		startButton.onClick.AddListener(StartGame);

		leftButton.SetActive(false);
		rightButton.SetActive(false);
		jumpButton.SetActive(false);
		pauseButton.SetActive(false);
		blue.SetActive(false);
		timer.SetActive(false);

	}

	public void StartGame(){
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
		Debug.Log(time.EndTimer());
	}

}
