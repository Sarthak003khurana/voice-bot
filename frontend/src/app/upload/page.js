"use client";

import { useState } from "react";
import axios from "axios";

export default function UploadPage() {

  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const uploadResume = async () => {

    if (!file) {
      alert("Please select a file");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {

      setLoading(true);

      const res = await axios.post(
        "http://127.0.0.1:8000/upload-resume",
        formData
      );

      console.log(res.data);

      alert("Resume uploaded successfully");

      window.location.href = "/interview";

    } catch (err) {

      console.log(err);

      alert("Upload failed");

    } finally {

      setLoading(false);
    }
  };

  return (
    <main className="h-screen bg-black text-white flex flex-col items-center justify-center">

      <h1 className="text-5xl font-bold mb-10">
        Upload Resume
      </h1>

      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
        className="mb-6"
      />

      <button
        onClick={uploadResume}
        disabled={loading}
        className="bg-white text-black px-8 py-3 rounded-xl font-semibold"
      >
        {loading ? "Uploading..." : "Upload Resume"}
      </button>

    </main>
  );
}
