"use client";

import { useState, useRef, useEffect, use } from "react";
import Link from "next/link";
import { askQuestion } from "@/lib/api";
import styles from "./page.module.css";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  loading?: boolean;
}

export default function ChatPage({
  params,
  searchParams,
}: {
  params: Promise<{ docId: string }>;
  searchParams: Promise<{ name?: string }>;
}) {
  const { docId } = use(params);
  const { name } = use(searchParams);
  const docName = name ? decodeURIComponent(name) : "Document";

  const [messages, setMessages] = useState<Message[]>([
    {
      id: "welcome",
      role: "assistant",
      content: `I've finished indexing **${docName}**. Ask me anything about it — I'll answer using only what's in the document.`,
    },
  ]);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async () => {
    const q = input.trim();
    if (!q || sending) return;
    setInput("");

    const userMsg: Message = { id: crypto.randomUUID(), role: "user", content: q };
    const loadingMsg: Message = { id: "loading", role: "assistant", content: "", loading: true };
    setMessages((prev) => [...prev, userMsg, loadingMsg]);
    setSending(true);

    try {
      const { answer } = await askQuestion(q, docId);
      setMessages((prev) =>
        prev.map((m) =>
          m.id === "loading" ? { id: crypto.randomUUID(), role: "assistant", content: answer } : m
        )
      );
    } catch (err: unknown) {
      const errMsg = err instanceof Error ? err.message : "Something went wrong.";
      setMessages((prev) =>
        prev.map((m) =>
          m.id === "loading"
            ? { id: crypto.randomUUID(), role: "assistant", content: `⚠ ${errMsg}` }
            : m
        )
      );
    } finally {
      setSending(false);
      inputRef.current?.focus();
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  // Auto-grow textarea
  const handleInput = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInput(e.target.value);
    e.target.style.height = "auto";
    e.target.style.height = Math.min(e.target.scrollHeight, 160) + "px";
  };

  return (
    <div className={styles.layout}>
      {/* Sidebar */}
      <aside className={styles.sidebar}>
        <Link href="/" id="back-home-link" className={styles.logo} aria-label="Back to home">
          <span className={styles.logoMark}>✦</span>
          <span className={styles.logoText}>Spoon</span>
        </Link>

        <div className={styles.docCard}>
          <div className={styles.docIcon} aria-hidden>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
              <polyline points="14 2 14 8 20 8"/>
            </svg>
          </div>
          <div className={styles.docMeta}>
            <span className={styles.docName}>{docName}</span>
            <span className={styles.docId}>ID: {docId.slice(0, 8)}…</span>
          </div>
        </div>

        <nav className={styles.sideNav}>
          <p className={styles.sideNavLabel}>Tips</p>
          <ul className={styles.tipList}>
            {[
              "Ask for a summary of the document",
              "Request specific sections or lists",
              "Ask follow-up questions",
              "Shift+Enter for a new line",
            ].map((tip) => (
              <li key={tip} className={styles.tip}>
                <span className={styles.tipDot} aria-hidden>·</span>
                {tip}
              </li>
            ))}
          </ul>
        </nav>

        <Link href="/" id="new-document-link" className={styles.newDocBtn}>
          + New document
        </Link>
      </aside>

      {/* Chat area */}
      <main className={styles.chatArea} id="chat-main">
        <header className={styles.chatHeader}>
          <Link href="/" id="mobile-back-link" className={styles.mobileBack} aria-label="Back">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <polyline points="15 18 9 12 15 6"/>
            </svg>
          </Link>
          <span className={styles.headerTitle}>{docName}</span>
        </header>

        <div className={styles.messages} role="log" aria-live="polite" aria-label="Chat messages">
          {messages.map((msg) => (
            <div
              key={msg.id}
              className={`${styles.msgRow} ${msg.role === "user" ? styles.userRow : styles.assistantRow}`}
            >
              {msg.role === "assistant" && (
                <div className={styles.avatar} aria-hidden>✦</div>
              )}
              <div className={`${styles.bubble} ${msg.role === "user" ? styles.userBubble : styles.aiBubble}`}>
                {msg.loading ? (
                  <span className={styles.typingDots} aria-label="Thinking">
                    <span /><span /><span />
                  </span>
                ) : (
                  <span className={styles.msgContent}>{msg.content}</span>
                )}
              </div>
            </div>
          ))}
          <div ref={bottomRef} />
        </div>

        {/* Input */}
        <div className={styles.inputBar}>
          <div className={styles.inputWrap}>
            <textarea
              ref={inputRef}
              id="chat-input"
              className={styles.textarea}
              placeholder="Ask a question about the document…"
              value={input}
              onChange={handleInput}
              onKeyDown={handleKeyDown}
              rows={1}
              aria-label="Question input"
              disabled={sending}
            />
            <button
              id="send-btn"
              className={styles.sendBtn}
              onClick={handleSend}
              disabled={!input.trim() || sending}
              aria-label="Send message"
            >
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <line x1="22" y1="2" x2="11" y2="13"/>
                <polygon points="22 2 15 22 11 13 2 9 22 2"/>
              </svg>
            </button>
          </div>
          <p className={styles.inputHint}>Enter to send · Shift+Enter for new line</p>
        </div>
      </main>
    </div>
  );
}
