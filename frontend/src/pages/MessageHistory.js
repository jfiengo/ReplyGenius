import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { messageApi } from '../api/api';

function MessageHistory() {
  const { phoneNumber } = useParams();
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchMessages = async () => {
      try {
        const response = await messageApi.getHistory(phoneNumber);
        setMessages(response.data);
      } catch (err) {
        setError(err.response?.data?.error || 'Error loading messages');
      } finally {
        setLoading(false);
      }
    };

    fetchMessages();
  }, [phoneNumber]);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 p-4 rounded-md">
        <div className="flex">
          <div className="ml-3">
            <h3 className="text-sm font-medium text-red-800">Error loading messages</h3>
            <div className="mt-2 text-sm text-red-700">{error}</div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div>
      <div className="sm:flex sm:items-center">
        <div className="sm:flex-auto">
          <h1 className="text-2xl font-semibold text-gray-900">Message History</h1>
          <p className="mt-2 text-sm text-gray-700">
            Conversation history for {phoneNumber}
          </p>
        </div>
      </div>
      <div className="mt-8 flow-root">
        <div className="-mx-4 -my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
          <div className="inline-block min-w-full py-2 align-middle sm:px-6 lg:px-8">
            <div className="overflow-hidden shadow ring-1 ring-black ring-opacity-5 sm:rounded-lg">
              <div className="divide-y divide-gray-200">
                {messages.map((message) => (
                  <div
                    key={message.id}
                    className={`p-4 ${
                      message.direction === 'inbound' ? 'bg-gray-50' : 'bg-white'
                    }`}
                  >
                    <div className="flex items-start space-x-3">
                      <div className="flex-1">
                        <div className="flex items-center justify-between">
                          <p className="text-sm font-medium text-gray-900">
                            {message.direction === 'inbound' ? 'Customer' : 'Business'}
                          </p>
                          <p className="text-sm text-gray-500">
                            {new Date(message.sent_at).toLocaleString()}
                          </p>
                        </div>
                        <p className="mt-1 text-sm text-gray-700">{message.content}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default MessageHistory; 