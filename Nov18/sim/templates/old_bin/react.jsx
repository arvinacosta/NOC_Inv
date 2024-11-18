import React, { useState, useRef, useEffect } from 'react';
import { Share, Pencil, Trash, MoreVertical, X } from 'lucide-react';

const TableRowWithActions = () => {
  const [showPopup, setShowPopup] = useState(false);
  const [activeModal, setActiveModal] = useState(null);
  const popupRef = useRef(null);

  // Close popup when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (popupRef.current && !popupRef.current.contains(event.target)) {
        setShowPopup(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Modal component
  const Modal = ({ title, isOpen, onClose }) => {
    if (!isOpen) return null;

    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white rounded-lg w-full max-w-md">
          <div className="flex justify-between items-center p-4 border-b">
            <h5 className="text-lg font-semibold">{title} Action</h5>
            <button onClick={onClose} className="p-1">
              <X size={20} />
            </button>
          </div>
          <div className="p-4">
            You clicked the "{title}" button{title === 'Delete' ? ' with Idx: 1' : ''}.
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="container mx-auto p-4">
      <table className="min-w-full border-collapse border border-gray-200">
        <tbody>
          <tr className="border-b">
            <td className="p-3 border">data1</td>
            <td className="p-3 border">data2</td>
            <td className="p-3 border">data3</td>
            <td className="p-3 border">data4</td>
            <td className="p-3 border">data5</td>
            <td className="p-3 border">data6</td>
            <td className="p-3 border relative">
              <button 
                onClick={() => setShowPopup(!showPopup)}
                className="p-2 hover:bg-gray-100 rounded-full"
              >
                <MoreVertical size={20} />
              </button>
              
              {showPopup && (
                <div 
                  ref={popupRef}
                  className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg z-10 border"
                >
                  <div className="py-1">
                    <button
                      onClick={() => {
                        setActiveModal('Disable');
                        setShowPopup(false);
                      }}
                      className="flex items-center px-4 py-2 text-sm text-blue-600 hover:bg-blue-50 w-full"
                    >
                      <Share size={16} className="mr-2" />
                      Disable
                    </button>
                    <button
                      onClick={() => {
                        setActiveModal('Modify');
                        setShowPopup(false);
                      }}
                      className="flex items-center px-4 py-2 text-sm text-yellow-600 hover:bg-yellow-50 w-full"
                    >
                      <Pencil size={16} className="mr-2" />
                      Modify
                    </button>
                    <button
                      onClick={() => {
                        setActiveModal('Delete');
                        setShowPopup(false);
                      }}
                      className="flex items-center px-4 py-2 text-sm text-red-600 hover:bg-red-50 w-full"
                    >
                      <Trash size={16} className="mr-2" />
                      Delete Idx: 1
                    </button>
                  </div>
                </div>
              )}
            </td>
          </tr>
        </tbody>
      </table>

      <Modal
        title={activeModal}
        isOpen={!!activeModal}
        onClose={() => setActiveModal(null)}
      />
    </div>
  );
};

export default TableRowWithActions;