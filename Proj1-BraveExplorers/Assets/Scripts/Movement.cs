using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class Movement : MonoBehaviour {

	public GameObject character;
	public float speed = 100;
	public Button leftButton, rightButton, jumpButton;
	
	void Start () {
		leftButton.onClick.AddListener(MoveLeft);
		rightButton.onClick.AddListener(MoveRight);
		jumpButton.onClick.AddListener(Jump);
	}
	
	void MoveLeft() {
		character.transform.Translate(Vector3.left * Time.deltaTime);

	}

	void MoveRight() {
		character.transform.Translate(Vector3.right * Time.deltaTime);
	}

	void Jump() {
		character.transform.Translate(Vector3.up * speed * Time.deltaTime);
	}
}
