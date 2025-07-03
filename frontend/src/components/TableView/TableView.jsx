import React from "react";

const TableView = ({ header, table }) => {
    return (
        <>
        <table>
            <thead>
                <tr>
                    {header.map((head, index) => (
                        <th key={index}>{head}</th>
                    ))}
                </tr>
            </thead>
            <tbody>
                {table.map((row, index) => (
                    <tr key={index}>
                        {header.map((head, index1) => (
                            <td key={index1}>{row[head]}</td>
                        ))}
                    </tr>
                ))}
            </tbody>
        </table>
        </>
    );
};

export default TableView;