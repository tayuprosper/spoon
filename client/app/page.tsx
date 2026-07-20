"use client";

import { useState, useRef, useCallback } from "react";
import { useRouter } from "next/navigation";
import { uploadPdf } from "@/lib/api";
import styles from "./page.module.css";

export default function HomePage() {
  const router = useRouter();
  const inputRef = useRef<HTMLInputElement>(null);

  const [dragging, setDragging] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState<"idle" | "uploading" | "error">("idle");
  const [errorMsg, setErrorMsg] = useState("");

  const handleFile = useCallback((f: File) => {
    if (!f.name.toLowerCase().endsWith(".pdf")) {
      setErrorMsg("Only PDF files are supported.");
      setStatus("error");
      return;
    }
    setFile(f);
    setStatus("idle");
    setErrorMsg("");
  }, []);

  const onDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      setDragging(false);
      const f = e.dataTransfer.files[0];
      if (f) handleFile(f);
    },
    [handleFile]
  );

  const onInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0];
    if (f) handleFile(f);
  };

  const handleUpload = async () => {
    if (!file) return;
    setStatus("uploading");
    setErrorMsg("");
    try {
      const { doc_id } = await uploadPdf(file);
      router.push(`/chat/${doc_id}?name=${encodeURIComponent(file.name)}`);
    } catch (err: unknown) {
      setErrorMsg(err instanceof Error ? err.message : "Upload failed.");
      setStatus("error");
    }
  };

  return (
    <main className={styles.main}>
      {/* Background orbs */}
      <div className={styles.orb1} aria-hidden />
      <div className={styles.orb2} aria-hidden />

      <div className={styles.hero}>
        <div className={styles.badge}>✦ Powered by local AI</div>
        <h1 className={styles.heading}>
          Ask anything about
          <br />
          <span className={styles.gradient}>any document</span>
        </h1>
        <p className={styles.subheading}>
          Upload a PDF and get instant, accurate answers — no data leaves your machine.
        </p>
      </div>

      {/* Drop zone */}
      <div
        id="drop-zone"
        role="button"
        tabIndex={0}
        aria-label="Upload PDF by clicking or dragging a file here"
        className={`${styles.dropzone} ${dragging ? styles.dragging : ""} ${file ? styles.hasFile : ""}`}
        onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
        onDragLeave={() => setDragging(false)}
        onDrop={onDrop}
        onClick={() => inputRef.current?.click()}
        onKeyDown={(e) => e.key === "Enter" && inputRef.current?.click()}
      >
        <input
          ref={inputRef}
          id="file-input"
          type="file"
          accept=".pdf"
          className={styles.hiddenInput}
          onChange={onInputChange}
          aria-hidden
        />

        {file ? (
          <div className={styles.filePreview}>
            <div className={styles.fileIcon}>
              <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                <polyline points="14 2 14 8 20 8"/>
                <line x1="16" y1="13" x2="8" y2="13"/>
                <line x1="16" y1="17" x2="8" y2="17"/>
                <polyline points="10 9 9 9 8 9"/>
              </svg>
            </div>
            <div className={styles.fileInfo}>
              <span className={styles.fileName}>{file.name}</span>
              <span className={styles.fileSize}>{(file.size / 1024).toFixed(0)} KB</span>
            </div>
            <button
              id="change-file-btn"
              className={styles.changeBtn}
              onClick={(e) => { e.stopPropagation(); setFile(null); setStatus("idle"); }}
              aria-label="Remove selected file"
            >
              ✕
            </button>
          </div>
        ) : (
          <div className={styles.dropContent}>
            <div className={styles.uploadIcon} aria-hidden>
              <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                <polyline points="17 8 12 3 7 8"/>
                <line x1="12" y1="3" x2="12" y2="15"/>
              </svg>
            </div>
            <p className={styles.dropLabel}>
              {dragging ? "Release to upload" : "Drag & drop your PDF here"}
            </p>
            <p className={styles.dropSub}>or click to browse</p>
          </div>
        )}
      </div>

      {status === "error" && (
        <p className={styles.errorMsg} role="alert">⚠ {errorMsg}</p>
      )}

      <button
        id="upload-btn"
        className={styles.uploadBtn}
        onClick={handleUpload}
        disabled={!file || status === "uploading"}
        aria-disabled={!file || status === "uploading"}
      >
        {status === "uploading" ? (
          <span className={styles.btnLoading}>
            <span className={styles.spinner} aria-hidden /> Indexing document…
          </span>
        ) : (
          "Analyse Document →"
        )}
      </button>

      <p className={styles.hint}>Supports PDF files up to any size · Runs 100% locally</p>
    </main>
  );
}
