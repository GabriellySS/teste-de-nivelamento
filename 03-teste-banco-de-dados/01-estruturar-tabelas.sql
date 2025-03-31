CREATE TABLE demonstracoes_contabeis (
	id INT AUTO_INCREMENT PRIMARY KEY,
    data DATE NOT NULL,
    reg_ans INT NOT NULL,
    cd_conta_contabil INT NOT NULL,
    descricao VARCHAR(255) NOT NULL,
    vl_saldo_inicial DECIMAL(10,2) NOT NULL,
    vl_saldo_final DECIMAL(10,2) NOT NULL
);