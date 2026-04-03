import express from "express";
import path from "path";
import fs from "fs";
import multer from "multer";
import { exec } from "child_process";

const app = express();

app.set("view engine", "ejs");
app.use(express.static(path.join(path.resolve(), "public")));

app.listen(5000, () => {
    console.log("Server is running on port 5000.");
});

app.get("/", (req, res) => {
    res.render("index");
});

let uploadPath = path.join(path.resolve(), "data");
if (!fs.existsSync(uploadPath)) {
    fs.mkdirSync(uploadPath);
}

uploadPath = path.join(path.resolve(), "data", "uploads");
if (!fs.existsSync(uploadPath)) {
    fs.mkdirSync(uploadPath);
}

const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, uploadPath);
    },
    filename: function (req, file, cb) {
        cb(null, file.originalname);
    },
});
const upload = multer({ storage });

app.post("/save_file", upload.single("videos"), (req, res) => {
    const pythonScriptPath = path.join(path.resolve(), "mainScript.py");

    exec(`python "${pythonScriptPath}"`, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error executing script: ${error.message}`);
            return res.status(500).send("Error processing video");
        }
        if (stderr) {
            console.error(`Script stderr: ${stderr}`);
        }
        console.log(`Script stdout: ${stdout}`);
        res.redirect("/output");
    });
});

app.get("/output", (req, res) => {
    const dataFolderPath = path.join(
        path.resolve(),
        "public",
        "high_speed_frames"
    );

    fs.readdir(dataFolderPath, (err, items) => {
        if (err) {
            console.error("Error reading data folder:", err);
            return res.status(500).send("Internal Server Error");
        }

        res.render("output", { items });
    });
});
