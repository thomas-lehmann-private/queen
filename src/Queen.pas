(*
   @author  Thomas Lehmann
   @file    Queen.pas

   Copyright (c) 2016 Thomas Lehmann

   Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
   documentation files (the "Software"), to deal in the Software without restriction, including without limitation
   the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
   and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

   The above copyright notice and this permission notice shall be included in all copies
   or substantial portions of the Software.

   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
   INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
   IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
   DAMAGES OR OTHER LIABILITY,
   WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 *)
program Queen;

uses sysutils;

type
    TSolution = object
            m_columns:    array of Integer;
    end;

    TQueen = object
        private
            m_width:      Integer;              // width(=height
            m_lastRow:    Integer;              // last row index
            m_lastColumn: Integer;              // last column index
            m_columns:    array Of Integer;     // occupied/free columns
            m_diagonals1: array Of Integer;     // occupied/free diagonals "\"
            m_diagonals2: array Of Integer;     // occupied/free diagonals "/"
            m_solutions:  array Of TSolution;   // found solutions

        public
            constructor init(width: Integer);
            function    getWidth: Integer;
            function    getNumberOfSolutions: LongInt;
            procedure   runAlgorithm(row: Integer);
            procedure   printSolutions;
    end;

constructor TQueen.init(width: Integer);
var
    numberOfDiagonals: Integer;
    index:  Integer;
begin
    m_width      := width;
    m_lastRow    := width - 1;
    m_lastColumn := width - 1;

    numberOfDiagonals := 2 * m_width - 1;

    SetLength(m_columns, m_width);
    SetLength(m_diagonals1, numberOfDiagonals);
    SetLength(m_diagonals2, numberOfDiagonals);
    SetLength(m_solutions, 0);

    for index := 0 to m_width-1 do begin
        if index < m_width then begin
            m_columns[index] := -1;
        end;
        m_diagonals1[index] := 0;
        m_diagonals2[index] := 0;
    end;
end;

function TQueen.getWidth: Integer; begin
    getWidth := m_width;
end;

function TQueen.getNumberOfSolutions: LongInt; begin
    getNumberOfSolutions := Length(m_solutions);
end;

procedure TQueen.runAlgorithm(row: Integer);
var
    column:   Integer;
    ixDiag1:  Integer;
    ixDiag2:  Integer;
begin
    for column := 0 to m_lastColumn do begin
        if m_columns[column] >= 0 then
            continue;

        ixDiag1 := row + column;
        if m_diagonals1[ixDiag1] = 1 then
            continue;

        ixDiag2 := m_lastRow - row + column;
        if m_diagonals2[ixDiag2] = 1 then
            continue;

        m_columns[column] := row;
        m_diagonals1[ixDiag1] := 1;
        m_diagonals2[ixDiag2] := 1;

        if row = m_lastRow then begin
            SetLength(m_solutions, Length(m_solutions) + 1);
            m_solutions[Length(m_solutions)-1].m_columns := Copy(m_columns);
        end

        else begin
            runAlgorithm(row + 1);
        end;

        m_columns[column] := -1;
        m_diagonals1[ixDiag1] := 0;
        m_diagonals2[ixDiag2] := 0;
    end;
end;

procedure TQueen.printSolutions;
var
    index: integer;
    column: integer;
begin
    for index := 0 to Length(m_solutions)-1 do begin
        for column := 0 to m_width-1 do begin
            write('(', column+1, ',', m_solutions[index].m_columns[column]+1, ')');
        end;
        writeln('');
    end;
end;

var
    width: Integer;
    instance: TQueen;
    start: comp;
begin
    width := 8; {default}

    if ParamCount = 1 then begin
        width := StrToInt(ParamStr(1));
    end;

    instance.init(width);
    Writeln('Free Pascal');
    Writeln('Queen raster (', instance.getWidth, 'x', instance.getWidth, ')');
    start := TimeStampToMSecs(DateTimeToTimeStamp(Now));
    instance.runAlgorithm(0);
    Writeln('...took ', Format('%.5f',[(TimeStampToMSecs(DateTimeToTimeStamp(Now))-start)/1000.0]), ' seconds.');
    Writeln('...', instance.getNumberOfSolutions(), ' solutions found.');
    {instance.printSolutions();}
end.
