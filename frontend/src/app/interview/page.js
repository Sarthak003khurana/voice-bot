"use client";

import { useEffect, useState } from "react";
import axios from "axios";

export default function InterviewPage() {

  const [question, setQuestion] = useState("");

  const fetchQuestion = async () => {

    try {

      const res = await axios.get(
        "http://127.0.0.1:8000/question"
      );

      setQuestion(res.data.question);

    } catch (err) {

      console.log(err);
    }
  };

  useEffect(() => {
    fetchQuestion();
  }, []);

  return (
    <main className="h-screen bg-black text-white flex flex-col items-center justify-center">

      <h1 className="text-5xl font-bold mb-10">
        Interview Session
      </h1>

      <div className="bg-zinc-900 p-10 rounded-2xl w-[700px] text-center">

        <p className="text-2xl">
          {question || "Loading question..."}
        </p>

      </div>

    </main>
  );
}
