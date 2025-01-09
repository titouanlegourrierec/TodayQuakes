<!----------------------------------------------------------------------->
<a name="readme-top"></a>
<!----------------------------------------------------------------------->

<table width="100%" style="border: none;">
  <tr>
    <!-- <td align="left" style="border: none;"><b>LE GOURRIEREC Titouan</b></td> -->
    <td align="right" style="border: none;">
      <a href="https://www.linkedin.com/in/titouanlegourrierec"><img src="https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"></a>
      <a href="mailto:titouanlegourrierec@icloud.com"><img src="https://img.shields.io/badge/email-%23339933.svg?style=for-the-badge&logo=mail.ru&logoColor=white" alt="Mail"></a>
      <!-- <a href="https://titouanlegourrierec.github.io"><img src="https://img.shields.io/badge/website-%23323330.svg?style=for-the-badge&logo=About.me&logoColor=white" alt="Website"></a> -->
    </td>
  </tr>
</table>

<!----------------------------------------------------------------------->
<!----------------------------------------------------------------------->

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://x.com/TodayQuakes">
    <img src="assets/logo.png" alt="Logo" width="40%">
  </a>

  <p align="center">
    A Twitter bot that automatically posts a daily map of the previous day's earthquakes, providing real-time global seismic activity updates.<br /><br /> LE GOURRIEREC Titouan<br />
    <!-- <br />
    <a href="https://github.com/othneildrew/Best-README-Template"><strong>Explore the docs »</strong></a>
    <br /> -->
    <br />
    <!-- <a href="https://github.com/othneildrew/Best-README-Template">View Demo</a>
    ·
    <a href="https://github.com/othneildrew/Best-README-Template/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    · -->
    <a href="https://github.com/titouanlegourrierec/TodayQuakes/issues/new">Report a bug · Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#data">Data</a></li>
  </ol>
</details>

<!----------------------------------------------------------------------->
<!----------------------------------------------------------------------->

## About The Project

<p align="center">
  <img src="assets/earthquakes_2000_2023.png" width="95%">
</p>

This project is a Twitter bot that posts daily updates on global seismic activity. Using the USGS (United States Geological Survey) [API](https://www.usgs.gov/programs/earthquake-hazards), it fetches earthquake data from the previous day, including the total number of quakes and their distribution by magnitude. The bot then generates a visual map displaying the locations of the earthquakes and posts it on Twitter (X) via the [X API](https://developer.x.com/en/products/x-api).

<p align="center">
  <img src="assets/post.png" width="75%">
</p>

Features:
- Automatic daily data retrieval from the [USGS API](https://www.usgs.gov/programs/earthquake-hazards).
- Visual map generation of earthquakes worldwide.
- Summary of key statistics: total earthquakes and magnitude distribution.
- Automated posting on X (formerly Twitter) using the [X API](https://developer.x.com/en/products/x-api).

The main functions of the bot, including data retrieval, processing, plotting, and posting to Twitter, are defined in `DailyQuakes.py`. The automation logic is handled by `bot.py`, while logging configuration is managed by `config_logging.py`, with log messages saved to `log.txt` in the `log` directory. The daily execution of the bot is automated using GitHub Actions, with the workflow defined in `.github/workflows/bot.yml`. This setup ensures the bot runs daily without manual intervention, fetching data, generating visualizations, and posting updates seamlessly.

<!----------------------------------------------------------------------->
<p align="right">(<a href="#readme-top">back to top</a>)</p>
<!----------------------------------------------------------------------->


### Built With
* [![Python][Python-badge]][Python-url]
* ![GitHub_Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)
* ![X](https://img.shields.io/badge/X-%23000000.svg?style=for-the-badge&logo=X&logoColor=white)

<!----------------------------------------------------------------------->
<p align="right">(<a href="#readme-top">back to top</a>)</p>
<!----------------------------------------------------------------------->

## License

Distributed under the MIT License. See [`LICENSE`](https://github.com/titouanlegourrierec/TodayQuakes/blob/main/LICENCE) for more information.

<!----------------------------------------------------------------------->
<p align="right">(<a href="#readme-top">back to top</a>)</p>
<!----------------------------------------------------------------------->

## Contact

LE GOURRIEREC Titouan - [titouanlegourrierec@icloud.com](mailto:titouanlegourrierec@icloud.com)

Project Link: [https://github.com/titouanlegourrierec/TodayQuakes](https://github.com/titouanlegourrierec/TodayQuakes)


<!----------------------------------------------------------------------->
<p align="right">(<a href="#readme-top">back to top</a>)</p>
<!----------------------------------------------------------------------->


## Data

* [USGS](https://www.usgs.gov/programs/earthquake-hazards) : Earthquakes data

<!----------------------------------------------------------------------->
<p align="right">(<a href="#readme-top">back to top</a>)</p>
<!----------------------------------------------------------------------->



<!-- MARKDOWN LINKS & IMAGES -->


[Python-badge]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]: https://www.python.org

[X-badge]: ![X](https://img.shields.io/badge/X-%23000000.svg?style=for-the-badge&logo=X&logoColor=white)
[X-url]: https://x.com/TodayQuakes