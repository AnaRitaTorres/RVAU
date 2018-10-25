using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class Movement : MonoBehaviour {

	public enum JumpStatus {Grounded, GoingUp, GoingDown};

	public GameObject character;
	public Button leftButton, rightButton, jumpButton;
	bool grounded = true;
	public JumpStatus status = JumpStatus.Grounded;

	float jumpTime = 0.75f;
	float currTime = 0.0f;
	float currSpeed = 0.0f;
			
	void Start () {
		status = JumpStatus.Grounded;
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
		if (status != JumpStatus.Grounded) return;
		else {
			status = JumpStatus.GoingUp;
		}
	}

	void Update() {
		if (status != JumpStatus.Grounded) {
			if (status == JumpStatus.GoingUp) {
				currTime += Time.deltaTime;
				currSpeed = 0.18f;
				character.transform.Translate(Vector3.up * currSpeed * Time.deltaTime);
			}
			else {
				currTime += Time.deltaTime;
				currSpeed = -0.18f;
				character.transform.Translate(Vector3.up * currSpeed * Time.deltaTime);
			}
		}
		if (currTime >= jumpTime / 2 && currTime < jumpTime && status != JumpStatus.GoingDown) {
			currTime = jumpTime / 2;
			status = JumpStatus.GoingDown;
		}
		if (currTime >= jumpTime) {
			currTime = 0.0f;
			status = JumpStatus.Grounded;
			currSpeed = 0.0f;
		}
	}
}
