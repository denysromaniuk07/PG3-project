import React from 'react';
import { useUserInfoStore } from '../store';

const UserDebugInfo = () => {
    const { user, username, email, userId, accessToken, refreshToken, isAuthenticated } = useUserInfoStore((state) => state);

    return (
        <div className="fixed bottom-20 right-4 bg-black/90 text-white p-4 rounded-lg text-xs max-w-sm z-50 font-mono">
            <div className="font-bold mb-2 text-green-400">🔐 Auth Debug Info</div>
            <div className="space-y-1">
                <div><span className="text-gray-400">Authenticated:</span> {isAuthenticated ? '✅ Yes' : '❌ No'}</div>
                <div><span className="text-gray-400">Username:</span> {username || 'N/A'}</div>
                <div><span className="text-gray-400">Email:</span> {email || 'N/A'}</div>
                <div><span className="text-gray-400">User ID:</span> {userId || 'N/A'}</div>
                <div><span className="text-gray-400">Access Token:</span> {accessToken ? `${accessToken.substring(0, 20)}...` : 'N/A'}</div>
                <div><span className="text-gray-400">Refresh Token:</span> {refreshToken ? `${refreshToken.substring(0, 20)}...` : 'N/A'}</div>
                <div className="mt-2 pt-2 border-t border-gray-700">
                    <span className="text-gray-400">Full User Object:</span>
                    <pre className="mt-1 text-[10px] overflow-auto max-h-32">
                        {JSON.stringify(user, null, 2)}
                    </pre>
                </div>
            </div>
        </div>
    );
};

export default UserDebugInfo;
