using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using Vuforia;

public class LockObjects : MonoBehaviour, ITrackableEventHandler {

	public Button lockButton;
	public GameObject chaiseLong;
	public GameObject basketball;
	public GameObject books;
	public Camera secondCamera;
	private TrackableBehaviour mTrackableBehaviour;
		
	void Start () {

		mTrackableBehaviour = GetComponent<TrackableBehaviour>();
        if(mTrackableBehaviour) {
            mTrackableBehaviour.RegisterTrackableEventHandler(this);
        }

		lockButton.onClick.AddListener(LockInPlace);	
	}

	public void OnTrackableStateChanged(TrackableBehaviour.Status previousStatus, TrackableBehaviour.Status newStatus) {
			//still need to touch up this function, not even being called
		if (newStatus == TrackableBehaviour.Status.DETECTED || newStatus == TrackableBehaviour.Status.TRACKED || newStatus == TrackableBehaviour.Status.EXTENDED_TRACKED) {
			
			//save name/id of marker and save it in variable 
			Debug.Log("Detetou Cenas");
		}
		else {
			Debug.Log("mehhh");
		}
        
	}
	
	void LockInPlace() {

		//after obtaining tracked object, permit only one lock of each kind
		
		var newChaise = Instantiate(chaiseLong, chaiseLong.transform.position, chaiseLong.transform.rotation);
		newChaise.transform.parent = secondCamera.transform;
		newChaise.transform.localScale =  new Vector3(5, 5, 5);
		newChaise.transform.localPosition = new Vector3(newChaise.transform.position.x, 0.0f, -newChaise.transform.position.z);
		
		var newBasketball = Instantiate(basketball, basketball.transform.position, basketball.transform.rotation);
		newBasketball.transform.parent = secondCamera.transform;
		newBasketball.transform.localScale =  new Vector3(5, 5, 5);
		newBasketball.transform.localPosition = new Vector3(newBasketball.transform.position.x, 0.0f, -newBasketball.transform.position.z);

		var newBooks = Instantiate(books, books.transform.position, books.transform.rotation);
		newBooks.transform.parent = secondCamera.transform;
		newBooks.transform.localScale =  new Vector3(5, 5, 5);
	 	newBooks.transform.localPosition = new Vector3(newBooks.transform.position.x, 0.0f, -newBooks.transform.position.z);
	}

	// Update is called once per frame
	void Update () {
		
	}
}
