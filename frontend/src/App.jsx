import React, {useState} from "react";
import TableEditor from "./components/TableEditor";

const App = () => {
    const [data, setData] = useState(null);

    // Очистка данных файла
    const removeData = () => {
        setData(null);
    }

    // Загрузка файла на сервер
    const handleFileUpload = async (event) => {
        const file = event.target.files[0];
        if (file) {
            const formData = new FormData();
            formData.append("file", file);

            const response = await fetch("/api/files/upload", {
                method: "POST",
                body: formData,
            });

            if (response.ok) {
                const result = await response.json();
                setData(result.data);
            } else {
                alert("Ошибка загрузки файла!");
            }
        }
    };

    // Сохранение файла
    const handleSave = async () => {

        const response = await fetch("/api/files/save", {
            method: "POST",
            body: JSON.stringify({data}),
        });

        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = "edited_file.xml";
            a.click();
        } else {
            alert("Ошибка при сохранении файла!");
        }
    };


    return (
        <div className="main-container">
            {
                data ? (
                    <>
                        <TableEditor data={data} onUpdate={setData}/>
                        <button onClick={handleSave} className="save-button">
                            Сохранить файл
                        </button>
                        <button onClick={removeData} className="break-button">
                            Отменить изменения
                        </button>
                    </>
                ) : (
                    <>
                        <h1>Добро пожаловать!</h1>
                        <p>Загрузите XML-файл для редактирования</p>
                        <input className="file-input" type="file" accept=".xml" onChange={handleFileUpload}/>
                    </>
                )
            }
        </div>
    );
};

export default App;
