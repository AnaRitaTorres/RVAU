using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class Movement : MonoBehaviour {

	public enum JumpStatus {Grounded, GoingUp, GoingDown};
	public enum MoveStatus {Grounded, MovingLeft, MovingRight};

	public GameObject character;
	public Button leftButton, rightButton, jumpButton;
	public JumpStatus jstatus = JumpStatus.Grounded;
	public MoveStatus mstatus = MoveStatus.Grounded;

	float jumpTime = 0.75f;
	float currTime = 0.0f;
	float currJumpSpeed = 0.0f;
	float currDirectionalSpeed = 0.0f;
			
	void Start () {
		jstatus = JumpStatus.Grounded;
		mstatus = MoveStatus.Grounded;
		leftButton.onClick.AddListener(MoveLeft);
		rightButton.onClick.AddListener(MoveRight);
		jumpButton.onClick.AddListener(Jump);
	}
	
	void MoveLeft() {
		
		if (mstatus == MoveStatus.Grounded){
			character.transform.Rotate(Vector3.up * 180, Space.Self); 
			mstatus = MoveStatus.MovingLeft;
			currDirectionalSpeed = 0.1f; 
		}
		else if (mstatus == MoveStatus.MovingLeft) {
			character.transform.Rotate(Vector3.up * -180, Space.Self); 
			mstatus = MoveStatus.Grounded;
			currDirectionalSpeed = 0.0f;
		}
	}

	void MoveRight() {
		if (mstatus == MoveStatus.Grounded){ 
			mstatus = MoveStatus.MovingRight;
			currDirectionalSpeed = 0.1f; 
		}
		else if (mstatus == MoveStatus.MovingRight) {
			mstatus = MoveStatus.Grounded;
			currDirectionalSpeed = 0.0f;
		}
	}

	void Jump() {
		if (jstatus != JumpStatus.Grounded) return;
		else {
			jstatus = JumpStatus.GoingUp;
		}
	}

	void Update() {

		// Jumping behaviour

		if (jstatus != JumpStatus.Grounded) {
			if (jstatus == JumpStatus.GoingUp) {
				currTime += Time.deltaTime;
				currJumpSpeed = 0.18f;
				character.transform.Translate(Vector3.up * currJumpSpeed * Time.deltaTime);
			}
			else {
				currTime += Time.deltaTime;
				currJumpSpeed = -0.18f;
				character.transform.Translate(Vector3.up * currJumpSpeed * Time.deltaTime);
			}
		}
		if (currTime >= jumpTime / 2 && currTime < jumpTime && jstatus != JumpStatus.GoingDown) {
			currTime = jumpTime / 2;
			jstatus = JumpStatus.GoingDown;
		}
		if (currTime >= jumpTime) {
			currTime = 0.0f;
			jstatus = JumpStatus.Grounded;
			currJumpSpeed = 0.0f;
		}

		// Moving Behaviour
		if (mstatus != MoveStatus.Grounded){
			character.transform.Translate(Vector3.forward * currDirectionalSpeed * Time.deltaTime);
		}

	}
}
