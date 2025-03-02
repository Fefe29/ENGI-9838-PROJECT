import { useState, useRef } from "react";
import { Webcam } from "../utils/webcam";

const ButtonHandler = ({ imageRef, cameraRef, videoRef }) => {
  const [streaming, setStreaming] = useState(null); // streaming state
  const inputImageRef = useRef(null); // video input reference
  const inputVideoRef = useRef(null); // video input reference
  const webcam = new Webcam(); // webcam handler

  // closing image
  const closeImage = () => {
    const url = imageRef.current.src;
    imageRef.current.src = "#"; // restore image source
    URL.revokeObjectURL(url); // revoke url

    setStreaming(null); // set streaming to null
    inputImageRef.current.value = ""; // reset input image
    imageRef.current.style.display = "none"; // hide image
  };

  // closing video streaming
  const closeVideo = () => {
    const url = videoRef.current.src;
    videoRef.current.src = ""; // restore video source
    URL.revokeObjectURL(url); // revoke url

    setStreaming(null); // set streaming to null
    inputVideoRef.current.value = ""; // reset input video
    videoRef.current.style.display = "none"; // hide video
  };

  // opening front-facing camera
  const openFrontCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: "user" }, // Use "user" to specify the front camera
        audio: false,
      });
      cameraRef.current.srcObject = stream; // Attach the stream to the camera element
      cameraRef.current.style.display = "block"; // Show the camera
      setStreaming("frontCamera"); // Update the streaming state
    } catch (error) {
      alert("Error accessing front camera: " + error.message);
    }
  };

  // closing front-facing camera
  const closeFrontCamera = () => {
    const tracks = cameraRef.current.srcObject?.getTracks();
    tracks?.forEach((track) => track.stop()); // Stop all tracks
    cameraRef.current.srcObject = null; // Remove the video source
    cameraRef.current.style.display = "none"; // Hide the camera
    setStreaming(null); // Reset streaming state
  };

  return (
    <div className="btn-container">
      {/* Image Handler */}
      <input
        type="file"
        accept="image/*"
        style={{ display: "none" }}
        onChange={(e) => {
          const url = URL.createObjectURL(e.target.files[0]); // create blob url
          imageRef.current.src = url; // set image source
          imageRef.current.style.display = "block"; // show image
          setStreaming("image"); // set streaming to image
        }}
        ref={inputImageRef}
      />
      <button
        onClick={() => {
          if (streaming === null) inputImageRef.current.click();
          else if (streaming === "image") closeImage();
          else alert(`Can't handle more than 1 stream\nCurrently streaming : ${streaming}`);
        }}
      >
        {streaming === "image" ? "Close Image" : "Open Image"}
      </button>

      {/* Video Handler */}
      <input
        type="file"
        accept="video/*"
        style={{ display: "none" }}
        onChange={(e) => {
          if (streaming === "image") closeImage(); // closing image streaming
          const url = URL.createObjectURL(e.target.files[0]); // create blob url
          videoRef.current.src = url; // set video source
          videoRef.current.addEventListener("ended", () => closeVideo()); // add ended video listener
          videoRef.current.style.display = "block"; // show video
          setStreaming("video"); // set streaming to video
        }}
        ref={inputVideoRef}
      />
      <button
        onClick={() => {
          if (streaming === null || streaming === "image") inputVideoRef.current.click();
          else if (streaming === "video") closeVideo();
          else alert(`Can't handle more than 1 stream\nCurrently streaming : ${streaming}`);
        }}
      >
        {streaming === "video" ? "Close Video" : "Open Video"}
      </button>

      {/* Webcam Handler */}
      <button
        onClick={() => {
          if (streaming === null || streaming === "image") {
            if (streaming === "image") closeImage();
            webcam.open(cameraRef.current); // open webcam
            cameraRef.current.style.display = "block"; // show camera
            setStreaming("camera"); // set streaming to camera
          } else if (streaming === "camera") {
            webcam.close(cameraRef.current);
            cameraRef.current.style.display = "none";
            setStreaming(null);
          } else alert(`Can't handle more than 1 stream\nCurrently streaming : ${streaming}`);
        }}
      >
        {streaming === "camera" ? "Close Webcam" : "Open Webcam"}
      </button>

      {/* Front Camera Handler */}
      <button
        onClick={() => {
          if (streaming === null || streaming !== "frontCamera") {
            if (streaming === "camera") webcam.close(cameraRef.current);
            openFrontCamera(); // Open front-facing camera
          } else {
            closeFrontCamera(); // Close front-facing camera
          }
        }}
      >
        {streaming === "frontCamera" ? "Close Front Camera" : "Open Front Camera"}
      </button>
    </div>
  );
};

export default ButtonHandler;
