using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class Movement : MonoBehaviour {

	public GameObject character;
	
	public Button leftButton, rightButton;
	
	void Start () {
		leftButton.onClick.AddListener(MoveLeft);
		rightButton.onClick.AddListener(MoveRight);
	}
	
	void MoveLeft() {
		character.transform.Translate(Vector3.left * Time.deltaTime);

	}

	void MoveRight() {
		character.transform.Translate(Vector3.right * Time.deltaTime);
	}
}
