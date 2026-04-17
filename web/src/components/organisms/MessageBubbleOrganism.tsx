import React from 'react';
import { Message } from '../../types/api.types';
import { MessageBubble as MessageBubbleComponent } from '../molecules/MessageBubble/MessageBubble';

interface MessageBubbleProps {
  message: Message;
}

export const MessageBubbleOrganism: React.FC<MessageBubbleProps> = ({ 
  message 
}) => {
  return <MessageBubbleComponent message={message} />;
};

export default MessageBubbleOrganism;
