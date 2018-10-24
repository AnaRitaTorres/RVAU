using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class Movement : MonoBehaviour {

	public GameObject character;
	public Button leftButton, rightButton, jumpButton;
	bool grounded;
			
	void Start () {
		
		grounded = true;
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
		
		if(grounded) {
			character.transform.Translate(Vector3.up * Time.deltaTime);
			grounded = false;
		}
		else {
		    character.transform.Translate(-Vector3.up * Time.deltaTime);
			grounded = true;
		}
		
	}
}
