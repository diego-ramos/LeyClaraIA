import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { Send, Mic, Volume2, Paperclip, FileText, Youtube, AlertCircle, CheckCircle } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

const API_URL = 'http://localhost:8000';

export default function ChatInterface() {
    const [messages, setMessages] = useState([
        { role: 'assistant', content: 'Hola! Soy TeLoExplico. Sube tus documentos legales y pregúntame lo que quieras. Te lo explicaré fácil.' }
    ]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [files, setFiles] = useState([]);
    const [isUploading, setIsUploading] = useState(false);
    const [uploadStatus, setUploadStatus] = useState('');
    const [isListening, setIsListening] = useState(false);

    const messagesEndRef = useRef(null);
    const fileInputRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    // Voice Recognition (Speech to Text)
    const startListening = () => {
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            const recognition = new SpeechRecognition();
            recognition.lang = 'es-ES';
            recognition.continuous = false;
            recognition.interimResults = false;

            recognition.onstart = () => setIsListening(true);
            recognition.onend = () => setIsListening(false);
            recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                setInput(transcript);
            };

            recognition.start();
        } else {
            alert('Tu navegador no soporta reconocimiento de voz.');
        }
    };

    // Text to Speech
    const speakText = (text) => {
        if ('speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = 'es-ES';
            window.speechSynthesis.speak(utterance);
        }
    };

    const handleFileChange = (e) => {
        setFiles(Array.from(e.target.files));
    };

    const handleUpload = async () => {
        if (files.length === 0) return;
        setIsUploading(true);
        setUploadStatus('Subiendo e indexando...');

        const formData = new FormData();
        files.forEach(file => {
            formData.append('files', file);
        });

        try {
            await axios.post(`${API_URL}/upload`, formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });
            setUploadStatus('¡Documentos listos! Ya puedes preguntar.');
            setFiles([]);
        } catch (error) {
            console.error("Upload error:", error);
            setUploadStatus('Error al subir documentos.');
        } finally {
            setIsUploading(false);
        }
    };

    const handleSend = async () => {
        if (!input.trim()) return;

        const userMessage = { role: 'user', content: input };
        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setIsLoading(true);

        try {
            const response = await axios.post(`${API_URL}/chat`, { message: userMessage.content });
            const botMessage = {
                role: 'assistant',
                content: response.data.answer,
                sources: response.data.sources,
                confidence: response.data.confidence_score,
                videos: response.data.youtube_videos
            };
            setMessages(prev => [...prev, botMessage]);

            // Auto-speak if it was a voice interaction (optional, but nice)
            // speakText(botMessage.content); 
        } catch (error) {
            console.error("Chat error:", error);
            setMessages(prev => [...prev, { role: 'assistant', content: 'Lo siento, hubo un error al procesar tu pregunta.' }]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    return (
        <div className="flex flex-col h-screen bg-gray-50">
            {/* Header */}
            <header className="bg-white shadow-sm p-4 flex items-center justify-between">
                <h1 className="text-2xl font-bold text-primary flex items-center gap-2">
                    <FileText className="w-8 h-8" />
                    TeLoExplico
                </h1>
                <div className="flex items-center gap-4">
                    {/* File Upload Area */}
                    <div className="flex items-center gap-2 bg-gray-100 p-2 rounded-lg">
                        <input
                            type="file"
                            multiple
                            ref={fileInputRef}
                            onChange={handleFileChange}
                            className="hidden"
                            accept=".pdf,.txt"
                        />
                        <button
                            onClick={() => fileInputRef.current.click()}
                            className="text-gray-600 hover:text-primary transition"
                            title="Adjuntar documentos"
                        >
                            <Paperclip className="w-5 h-5" />
                        </button>
                        {files.length > 0 && (
                            <span className="text-xs font-medium text-gray-700">{files.length} archivo(s)</span>
                        )}
                        <button
                            onClick={handleUpload}
                            disabled={files.length === 0 || isUploading}
                            className={`px-3 py-1 rounded text-sm font-medium transition ${files.length === 0 ? 'bg-gray-300 text-gray-500' : 'bg-primary text-white hover:bg-blue-700'}`}
                        >
                            {isUploading ? '...' : 'Subir'}
                        </button>
                    </div>
                    {uploadStatus && <span className="text-xs text-green-600 font-medium">{uploadStatus}</span>}
                </div>
            </header>

            {/* Chat Area */}
            <main className="flex-1 overflow-y-auto p-4 space-y-6">
                {messages.map((msg, idx) => (
                    <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                        <div className={`max-w-[80%] rounded-2xl p-4 shadow-sm ${msg.role === 'user' ? 'bg-primary text-white rounded-br-none' : 'bg-white text-gray-800 rounded-bl-none border border-gray-100'}`}>
                            <ReactMarkdown className="prose prose-sm max-w-none">
                                {msg.content}
                            </ReactMarkdown>

                            {/* Bot Extras: Sources, Confidence, Videos */}
                            {msg.role === 'assistant' && (
                                <div className="mt-4 space-y-3">
                                    {/* Controls */}
                                    <div className="flex items-center gap-2 border-t pt-2">
                                        <button onClick={() => speakText(msg.content)} className="text-gray-500 hover:text-primary" title="Leer en voz alta">
                                            <Volume2 className="w-4 h-4" />
                                        </button>
                                        {msg.confidence && (
                                            <div className={`flex items-center gap-1 text-xs font-medium px-2 py-1 rounded-full ${msg.confidence === 'High' ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'}`}>
                                                {msg.confidence === 'High' ? <CheckCircle className="w-3 h-3" /> : <AlertCircle className="w-3 h-3" />}
                                                Confianza: {msg.confidence === 'High' ? 'Alta' : 'Media'}
                                            </div>
                                        )}
                                    </div>

                                    {/* Sources */}
                                    {msg.sources && msg.sources.length > 0 && (
                                        <details className="group">
                                            <summary className="cursor-pointer text-xs text-gray-500 font-medium hover:text-primary list-none flex items-center gap-1">
                                                <span>▶ Ver Fuentes ({msg.sources.length})</span>
                                            </summary>
                                            <div className="mt-2 space-y-2 pl-2 border-l-2 border-gray-200">
                                                {msg.sources.map((source, i) => (
                                                    <div key={i} className="text-xs text-gray-600">
                                                        <p className="italic">"{source.content}"</p>
                                                        <p className="font-semibold mt-1">— {source.source} (Pág. {source.page})</p>
                                                    </div>
                                                ))}
                                            </div>
                                        </details>
                                    )}

                                    {/* Videos */}
                                    {msg.videos && msg.videos.length > 0 && (
                                        <div className="mt-3">
                                            <p className="text-xs font-bold text-gray-500 mb-2 flex items-center gap-1"><Youtube className="w-4 h-4 text-red-600" /> Videos Relacionados</p>
                                            <div className="flex gap-3 overflow-x-auto pb-2">
                                                {msg.videos.map((video, i) => (
                                                    <a key={i} href={`https://www.youtube.com/watch?v=${video.videoId}`} target="_blank" rel="noopener noreferrer" className="min-w-[160px] group">
                                                        <div className="relative rounded-lg overflow-hidden aspect-video">
                                                            <img src={video.thumbnail} alt={video.title} className="w-full h-full object-cover group-hover:scale-105 transition" />
                                                            <div className="absolute inset-0 bg-black/20 group-hover:bg-black/0 transition" />
                                                        </div>
                                                        <p className="text-xs font-medium mt-1 line-clamp-2 group-hover:text-primary">{video.title}</p>
                                                    </a>
                                                ))}
                                            </div>
                                        </div>
                                    )}
                                </div>
                            )}
                        </div>
                    </div>
                ))}
                {isLoading && (
                    <div className="flex justify-start">
                        <div className="bg-white p-4 rounded-2xl rounded-bl-none shadow-sm border border-gray-100">
                            <div className="flex gap-1">
                                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                            </div>
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </main>

            {/* Input Area */}
            <footer className="bg-white p-4 border-t">
                <div className="max-w-4xl mx-auto flex items-center gap-2">
                    <button
                        onClick={startListening}
                        className={`p-3 rounded-full transition ${isListening ? 'bg-red-100 text-red-600 animate-pulse' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'}`}
                        title="Hablar"
                    >
                        <Mic className="w-5 h-5" />
                    </button>
                    <div className="flex-1 relative">
                        <textarea
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyDown={handleKeyDown}
                            placeholder="Escribe tu pregunta legal aquí..."
                            className="w-full bg-gray-100 rounded-2xl px-4 py-3 pr-10 focus:outline-none focus:ring-2 focus:ring-primary/50 resize-none h-[50px]"
                        />
                    </div>
                    <button
                        onClick={handleSend}
                        disabled={!input.trim() || isLoading}
                        className="p-3 bg-primary text-white rounded-full hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition"
                    >
                        <Send className="w-5 h-5" />
                    </button>
                </div>
            </footer>
        </div>
    );
}
