import React from "react";

const RecursiveTable = ({data, onUpdate}) => {
    const hasAttributes = data.some((row) => row.attributes && Object.keys(row.attributes).length > 0);
    const hasChildren = data.some((row) => row.children && row.children.length > 0);
    const hasText = data.some((row) => row.text && row.text.value !== "");

    const handleInputChange = (rowIndex, key, subKey, value) => {
        const updatedData = [...data];
        const updatedRow = {...updatedData[rowIndex]};

        if (key === "attributes") {
            updatedRow.attributes = {...updatedRow.attributes, [subKey]: {...updatedRow.attributes[subKey], value}};
        } else if (key === "text") {
            updatedRow.text = {...updatedRow.text, value};
        }

        updatedData[rowIndex] = updatedRow;
        onUpdate(updatedData);
    };

    const handleChildUpdate = (rowIndex, updatedChild) => {
        const updatedData = [...data];
        updatedData[rowIndex] = {...updatedData[rowIndex], children: updatedChild};
        onUpdate(updatedData);

    };

    const renderAttributes = (attributes, rowIndex) =>
        Object.entries(attributes).map(([attrKey, attrValue]) => (
            <div key={attrKey} className="attribute-container">
                <label className="attribute-label">{attrKey}:</label>
                <input
                    className="attribute-input"
                    type={attrValue.type}
                    value={attrValue.value || ""}
                    onChange={(e) => handleInputChange(rowIndex, "attributes", attrKey, e.target.value)}
                />
            </div>
        ));

    const renderText = (text, rowIndex) => (
        <div className="text-container">
            <input
                className="text-input"
                type={text.type}
                value={text.value || ""}
                onChange={(e) => handleInputChange(rowIndex, "text", "value", e.target.value || " ")}
            />
        </div>
    );

    const isSimpleRow = (row) =>
        (!row.attributes || Object.keys(row.attributes).length === 0) &&
        (!row.children || row.children.length === 0);

    return (
        <table className="recursive-table">

            <tbody>
            {data.map((row, rowIndex) => {
                if (isSimpleRow(row)) {
                    return (
                        <tr key={rowIndex}>
                            <td colSpan={hasAttributes + hasChildren + hasText + 1} className="simple-row">
                                <strong>{row.tag}:</strong> {row.text && renderText(row.text, rowIndex)}
                            </td>
                        </tr>
                    );
                }

                return (
                    <tr key={rowIndex}>
                        <td className="table-cell">{row.tag || "—"}</td>

                        {/* Столбец атрибутов */}
                        {hasAttributes && (
                            <td className="table-cell">
                                {row.attributes && Object.keys(row.attributes).length > 0
                                    ? renderAttributes(row.attributes, rowIndex)
                                    : "—"}
                            </td>
                        )}

                        {/* Столбец вложений */}
                        {hasChildren && (
                            <td className="table-cell">
                                {row.children && row.children.length > 0 ? (
                                    <RecursiveTable
                                        data={row.children}
                                        onUpdate={(updatedChild) => handleChildUpdate(rowIndex, updatedChild)}
                                    />
                                ) : "—"}
                            </td>
                        )}

                        {/* Текст */}
                        {hasText && (
                            <td className="table-cell">
                                {row.text && row.text.value ? renderText(row.text, rowIndex) : "—"}
                            </td>
                        )}
                    </tr>
                );
            })}
            </tbody>
        </table>
    );
};

const TableEditor = ({data, onUpdate}) => {
    return (
        <div className="table-editor-container">
            <h2>Редактирование файла</h2>
            <RecursiveTable data={data} onUpdate={onUpdate}/>
        </div>
    );
};

export default TableEditor;
