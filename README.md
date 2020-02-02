# OBIA4RTM-Agricultural-Example

This is a repository that was created within the I3 project **OBIA4RTM** at the University of Salzburg, Austria. It deals with **`object-based plant parameter retrieval from optical remotely sensed imagery`** (i.e., Sentinel-2) using **`radiative transfer models in an agricultural use case`**:

# Project Abstract

[OBIA4RTM](https://github.com/lukasValentin/OBIA4RTM) is an open-source **Python tool** that attempts to combine object-based image analysis (OBIA) methods with radiative transfer models (RTM) of vegetation to retrieve plant parameters from optical remotely sensed imagery (i.e. **Sentinel 2**) for different agricultural crop types. Currently, plant parameters such as the **leaf area index (LAI)** are retrieved operationally on a per-pixel base. Pixel-based approaches, however, neglect spatial autocorrelation. Moreover, the current usage of RTM is hampered by the ill-posed nature of radiative transfer theory as the inversion of the equations required to derive plant parameters cannot be done analytically and no unique solution to the inverse problem exists. The introduction of spatial constraints is therefore considered a way to reduce the ill-posedness of plant parameter retrieval and enhance the retrieval accuracy.

The proposed approach is assumed to deliver more meaningful and stable results about plant-parameters than pixel-based ones as the usage of spatial information is assumed to suppress noise inherent in satellite imagery. The end user – mainly individual farmers – could consequently benefit from more accurate and robust results. This is considered particularly important as shareholders and decision makers in agriculture demand up-to-date and reliable information about crop growing conditions to adjust farming practices accordingly.

To demonstrate and validate the OBIA4RTM tool an agricultural region in Southern Germany with in-situ measurements of plant-parameters over longer time periods available (collected by LMU Munich) is used as test site. In addition, scaling up the approach on the catchment scale located in a similar climatic regime (Upper Austria) is used to demonstrate the capacity of the tool to deal with larger amounts of data.

The whole workflow of the approach alongside with a in-depth analysis is available from a Jupyter notebook that was created to allow for a maximum level of interactivity:

# Project Jupyter Notebook

The core element of the whole project is this [Jupyter notebook](https://github.com/lukasValentin/OBIA4RTM-Agricultural-Example/blob/master/Deliverables/Jupyter-Notebook/analyse-visualise_OBIA4RTM.ipynb) that contains the most important analysis steps, the results and the use cases. All results saved to the database are available through the provided [database dump](https://github.com/lukasValentin/OBIA4RTM-Agricultural-Example/blob/master/database/obia4rtm_db_dump) that can be used to setup the database on any PostgreSQL DBMS and re-run the Jupyter notebook.
